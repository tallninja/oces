import sys
import subprocess
from datetime import date
from db.languages import languages
from models.submission import Submission
from utils.file import File
from jobs.config import (
    ENABLE_NETWORK,
    MEMORY_LIMIT,
    REDIRECT_STDERR_TO_STDOUT,
    CPU_TIME_LIMIT,
    MAX_CPU_TIME_LIMIT,
    CPU_EXTRA_TIME,
    WALL_TIME_LIMIT,
    MAX_WALL_TIME_LIMIT,
    STACK_LIMIT,
    MAX_STACK_LIMIT,
    MAX_PROCESSES_AND_OR_THREADS,
    MAX_MAX_PROCESSES_AND_OR_THREADS,
    ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT,
    ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT,
    MAX_FILE_SIZE
)

STDIN_FILE_NAME = 'stdin.txt'
STDOUT_FILE_NAME = 'stdout.txt'
STDERR_FILE_NAME = 'stderr.txt'
COMPILE_OUTPUT_FILE_NAME = 'compile_output.txt'
METADATA_FILE_NAME = 'metadata.txt'
COMPILE_FILE_NAME = 'compile'
RUN_FILE_NAME = 'run'


class IsolateJob:
    def __init__(self, workdir, submission: Submission):
        self.language = next(
            (lang for lang in languages if lang['name'] == submission.language), None)
        self.code = submission.code
        self.stdin = submission.stdin or ''
        self.box_id = submission.id % 2147483647
        self.workdir = workdir
        self.boxdir = f'{self.workdir}/box'
        self.tmpdir = f'{self.workdir}/tmp'
        self.source_file = self.boxdir + '/' + self.language.get('source_file')
        self.stdin_file = f'{self.boxdir}/{STDIN_FILE_NAME}'
        self.stdout_file = f'{self.boxdir}/{STDOUT_FILE_NAME}'
        self.stderr_file = f'{self.boxdir}/{STDERR_FILE_NAME}'
        self.compile_output = None
        self.compile_output_file = f'{self.boxdir}/{COMPILE_OUTPUT_FILE_NAME}'
        self.metadata_file = f'{self.boxdir}/{METADATA_FILE_NAME}'
        self.compile_script = f'{self.boxdir}/{COMPILE_FILE_NAME}'
        self.run_script = f'{self.boxdir}/{RUN_FILE_NAME}'

    @staticmethod
    def perform(submission: Submission):
        workdir = IsolateJob.create_sandbox(box_id=submission.id % 2147483647)
        print(workdir)
        job = IsolateJob(
            workdir=workdir,
            submission=submission
        )
        job.create_source_file()
        job.create_stdid_file()
        job.create_compile_script()
        job.create_run_script()
        if not job.compile_code():
            job.cleanup()
            return {'compile_output': job.compile_output}
        output = job.run_code()
        job.cleanup()
        return output

    @staticmethod
    def create_sandbox(box_id):
        init_cmd = f'isolate --cg -b {box_id} --init'
        return subprocess.run(init_cmd.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    def create_source_file(self):
        File.write_bytes(file=self.source_file, data=self.code)

    def create_stdid_file(self):
        File.write_bytes(file=self.stdin_file, data=self.stdin)

    def create_compile_script(self):
        File.write_bytes(
            file=self.compile_script,
            data=self.language.get('compile_cmd') or ''
        )

    def create_run_script(self):
        File.write_bytes(
            file=self.run_script,
            data=self.language.get('run_cmd')
        )

    def compile_code(self):
        compile_cmd = f'isolate --cg -s -b {self.box_id} \
                        --meta={self.metadata_file} \
                        --stdin=/dev/null\
                        --time={MAX_CPU_TIME_LIMIT} \
                        --extra-time=0 \
                        --wall-time={MAX_WALL_TIME_LIMIT} \
                        --stack={MAX_STACK_LIMIT} \
                        -p{MAX_MAX_PROCESSES_AND_OR_THREADS} \
                        {"--no-cg-timing" if ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT else "--cg-timing"} \
                        { "--mem=" if ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT else "--cg-mem=" }{MEMORY_LIMIT} \
                        --fsize={MAX_FILE_SIZE} \
                        --stderr-to-stdout \
                        --stdout={COMPILE_OUTPUT_FILE_NAME} \
                        -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/cargo/bin \
                        -E CARGO_HOME -E RUSTUP_HOME \
                        --run -- /bin/bash {COMPILE_FILE_NAME}'

        print(f'{date.today()} Compiling code')
        compile_command = subprocess.run(
            compile_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.compile_output = File.read_bytes(file=self.compile_output_file)
        cleanup_cmd = f'rm -rf {self.compile_output_file}'
        subprocess.run(cleanup_cmd.split())
        return compile_command.returncode == 0

    def run_code(self):
        run_cmd = f'isolate --cg -s -b {self.box_id} \
                    -M {self.metadata_file} \
                    {"--stderr-to-stdout" if REDIRECT_STDERR_TO_STDOUT else ""} \
                    {"--share-net" if ENABLE_NETWORK else ""} \
                    --time={CPU_TIME_LIMIT} \
                    --extra-time={CPU_EXTRA_TIME} \
                    --wall-time={WALL_TIME_LIMIT} \
                    --stack={STACK_LIMIT} \
                    -p{MAX_PROCESSES_AND_OR_THREADS} \
                    {"--no-cg-timing" if ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT else "--cg-timing"} \
                    { "--mem=" if ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT else "--cg-mem=" }{MEMORY_LIMIT} \
                    --fsize={MAX_FILE_SIZE} \
                    --stdin={STDIN_FILE_NAME} \
                    --stdout={STDOUT_FILE_NAME} \
                    --stderr={STDERR_FILE_NAME} \
                    -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/cargo/bin \
                    -E PATH -E CARGO_HOME -E RUSTUP_HOME \
                    -d /etc:noexec \
                    --run -- /bin/bash {RUN_FILE_NAME}'
        subprocess.run(run_cmd.split())
        return {
            'stdin': File.read_bytes(file=self.stdin_file),
            'stdout': File.read_bytes(file=self.stdout_file),
            'stderr': File.read_bytes(file=self.stderr_file),
            'metadata': self.get_metadata()
        }

    def get_metadata(self):
        metadata = {}
        for line in File.read(file=self.metadata_file).strip().split('\n'):
            pairs = line.split(':')
            key, value = pairs[0], pairs[1]
            metadata[key] = value
        return metadata

    def cleanup(self):
        rm_cmd = f'rm -rf {self.boxdir}/* {self.tmpdir}/*'
        cleanup_cmd = f'isolate --cg -b {self.box_id} --cleanup'
        subprocess.run(rm_cmd.split())
        subprocess.run(cleanup_cmd.split())
