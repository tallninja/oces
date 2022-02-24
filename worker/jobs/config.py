################################################################################
# Submission Configuration
################################################################################
# Judge0 uses isolate as an sandboxing environment.
# Almost all of the options you see here can be mapped to one of the options
# that isolate provides. For more information about these options please
# check for the isolate documentation here:
# https://raw.githubusercontent.com/ioi/isolate/master/isolate.1.txt

# Default runtime limit for every program (in seconds). Decimal numbers are allowed.
# Time in which the OS assigns the processor to different tasks is not counted.
# Default: 5
CPU_TIME_LIMIT = None

# Maximum custom CPU_TIME_LIMIT.
# Default: 15
MAX_CPU_TIME_LIMIT = None

# When a time limit is exceeded, wait for extra time (in seconds), before
# killing the program. This has the advantage that the real execution time
# is reported, even though it slightly exceeds the limit.
# Default: 1
CPU_EXTRA_TIME = None

# Maximum custom CPU_EXTRA_TIME.
# Default: 5
MAX_CPU_EXTRA_TIME = None

# Limit wall-clock time in seconds. Decimal numbers are allowed.
# This clock measures the time from the start of the program to its exit,
# so it does not stop when the program has lost the CPU or when it is waiting
# for an external event. We recommend to use CPU_TIME_LIMIT as the main limit,
# but set WALL_TIME_LIMIT to a much higher value as a precaution against
# sleeping programs.
# Default: 10
WALL_TIME_LIMIT = None

# Maximum custom WALL_TIME_LIMIT.
# Default: 20
MAX_WALL_TIME_LIMIT = None

# Limit address space of the program in kilobytes.
# Default: 128000
MEMORY_LIMIT = None

# Maximum custom MEMORY_LIMIT.
# Default: 512000
MAX_MEMORY_LIMIT = None

# Limit process stack in kilobytes.
# Default: 64000
STACK_LIMIT = None

# Maximum custom STACK_LIMIT.
# Default: 128000
MAX_STACK_LIMIT = None

# Maximum number of processes and/or threads program can create.
# Default: 60
MAX_PROCESSES_AND_OR_THREADS = None

# Maximum custom MAX_PROCESSES_AND_OR_THREADS.
# Default: 120
MAX_MAX_PROCESSES_AND_OR_THREADS = None

# If true then CPU_TIME_LIMIT will be used as per process and thread.
# Default: false, i.e. CPU_TIME_LIMIT is set as a total limit for all processes and threads.
ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT = None

# If false, user won't be able to set ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT.
# Default: true
ALLOW_ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT = None

# If true then MEMORY_LIMIT will be used as per process and thread.
# Default: false, i.e. MEMORY_LIMIT is set as a total limit for all processes and threads.
ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT = None

# If false, user won't be able to set ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT.
# Default: true
ALLOW_ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT = None

# Limit size of files created (or modified) by the program in kilobytes.
# Default: 1024
MAX_FILE_SIZE = None

# Maximum custom MAX_FILE_SIZE.
# Default: 4096
MAX_MAX_FILE_SIZE = None

# Run each program this many times and take average of time and memory.
# Default: 1
NUMBER_OF_RUNS = None

# Maximum custom NUMBER_OF_RUNS.
# Default: 20
MAX_NUMBER_OF_RUNS = None

# Redirect stderr to stdout.
# Default: false
REDIRECT_STDERR_TO_STDOUT = None

# Maximum total size (in kilobytes) of extracted files from additional files archive.
# Default: 10240, i.e. maximum of 10MB in total can be extracted.
MAX_EXTRACT_SIZE = None

# If false, user won't be able to set ENABLE_NETWORK.
# Default: true, i.e. allow user to permit or deny network calls from the submission.
ALLOW_ENABLE_NETWORK = None

# If true submission will by default be able to do network calls.
# Default: false, i.e. programs cannot do network calls.
ENABLE_NETWORK = None