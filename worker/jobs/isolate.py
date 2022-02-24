import sys
import subprocess
from datetime import date
from db.languages import languages
from models.models import Submission
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


class IsolateJob:
    def __init__(self, box_id, workdir, language,  code,  stdin):
        self.language = next(
            (lang for lang in languages if lang['name'] == language), None)
        self.code = code
        self.stdin = stdin
        self.box_id = box_id
        self.workdir = workdir
        self.boxdir = f'{self.workdir}/box'
        self.tmpdir = f'{self.workdir}/tmp'
        self.source_file = self.boxdir + '/' + self.language.get('source_file')
        self.stdin_file = f'{self.boxdir}/stdin.txt'
        self.stdout_file = f'{self.boxdir}/stdout.txt'
        self.stderr_file = f'{self.boxdir}/stderr.txt'
        self.compile_output = None
        self.compile_output_file = f'{self.boxdir}/compile.txt'
        self.metadata_file = f'{self.boxdir}/metadata.txt'
        self.compile_script = f'{self.boxdir}/compile'
        self.run_script = f'{self.boxdir}/run'

    @staticmethod
    def perform(box_id, submission: Submission):
        success = True
        failure = False
        language = submission.language
        code = submission.code
        stdin = submission.stdin or ''
        workdir = IsolateJob.create_sandbox(box_id=box_id)
        job = IsolateJob(box_id=box_id, workdir=workdir,
                         language=language, code=code, stdin=stdin)
        job.create_source_file()
        job.create_stdid_file()
        job.create_compile_script()
        job.create_run_script()
        if job.compile_code() == failure:
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
                        --stdout=compile.txt\
                        -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
                        --run -- /bin/bash compile'

        print(f'{date.today()} Compiling code')
        compile_command = subprocess.run(
            compile_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.compile_output = File.read_bytes(file=self.compile_output_file)

        return True if compile_command.returncode == 0 else False

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
                    --stdin=stdin.txt \
                    --stdout=stdout.txt \
                    --stderr=stderr.txt \
                    -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
                    --run -- /bin/bash run'
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
