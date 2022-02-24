import subprocess
from db.languages import languages
from utils.file import File

class IsolateJob:
    def __init__(self, box_id, workdir, language,  code,  stdin):
        self.language = next((lang for lang in languages if lang['name'] == language), None)
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
        self.metadata_file = f'{self.boxdir}/metadata.txt'
        self.compile_script = f'{self.boxdir}/compile'
        self.run_script = f'{self.boxdir}/run'
        
    @staticmethod
    def perform(box_id, submission):
        language = submission.get('language')
        code = submission.get('code')
        stdin = submission.get('stdin') or ''
        workdir = IsolateJob.create_sandbox(box_id=box_id)
        job = IsolateJob(box_id=box_id, workdir=workdir, language=language, code=code, stdin=stdin)
        job.create_source_file()
        job.create_stdid_file()
        job.create_compile_script()
        job.create_run_script()
        job.compile_code()
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
                        -M {self.metadata_file} --stderr-to-stdout \
                        -p120 \
                        -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
                        --run -- /bin/bash compile'  
        subprocess.run(compile_cmd.split())

    def run_code(self):
        run_cmd = f'isolate --cg -s -b {self.box_id} \
                    -M {self.metadata_file} \
                    -p120 \
                    --stdin=stdin.txt \
                    --stdout=stdout.txt \
                    --stderr=stderr.txt \
                    --run -- /bin/bash run'
        subprocess.run(run_cmd.split())
        return { 
            'stdin': File.read_bytes(file=self.stdin_file),
            'stdout': File.read_bytes(file=self.stdout_file),
            'stderr': File.read_bytes(file=self.stderr_file)
        }


    def cleanup(self):
        rm_cmd = f'rm -rf {self.boxdir}/* {self.tmpdir}/*'
        cleanup_cmd = f'isolate --cg -b {self.box_id} --cleanup'
        subprocess.run(rm_cmd.split())
        subprocess.run(cleanup_cmd.split())



