import os
import subprocess

def shell(command):
    return subprocess.run(command, stdout=subprocess.PIPE)

def create_sandbox(box_id):
    init_cmd = f'isolate --cg -b {box_id} --init'
    return shell(init_cmd.split()).stdout.decode('utf-8').strip()

def create_source_file(boxdir, data):
    with open(f'{boxdir}/main.c', 'wb') as file:
        file.write(bytes(data, 'utf-8'))

def create_run_script(boxdir, run_cmd):
    with open(f'{boxdir}/run', 'wb') as file:
        file.write(bytes(run_cmd, 'utf-8'))

def create_compile_script(boxdir, compile_cmd):
    with open(f'{boxdir}/compile', 'wb') as file:
        file.write(bytes(compile_cmd, 'utf-8'))

def compile_code(box_id, boxdir):
    metadata_file = f'{boxdir}/metadata.txt'
    compile_cmd = f'isolate --cg -s -b {box_id} \
                    -M {metadata_file} --stderr-to-stdout \
                    -p120 \
                    -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
                    --run -- /bin/bash compile'  
    os.system(compile_cmd)


def run(box_id, boxdir):
    stdin_file = f'{boxdir}/stdin.txt'
    stdout_file = f'{boxdir}/stdout.txt'
    stderr_file = f'{boxdir}/stderr.txt'
    metadata_file = f'{boxdir}/metadata.txt'
    run_cmd = f'isolate --cg -s -b {box_id} \
                -M {metadata_file} \
                -p120 \
                --stdin=stdin.txt \
                --stdout=stdout.txt \
                --stderr=stderr.txt \
                --run -- /bin/bash run'
    os.system(f'touch {stdin_file}')
    os.system(run_cmd)
    output = None
    try:
        with open(f'{stdout_file}', 'rb') as file:
            output = file.read().decode('utf-8').strip()
        return output
    except:
        print("File does not exist")

def cleanup(box_id, boxdir, tmpdir):
    rm_cmd = f'rm -rf {boxdir}/* {tmpdir}/*'
    os.system(rm_cmd)
    shell(['isolate', '--cg', '-b', f'{box_id}', '--cleanup'])
