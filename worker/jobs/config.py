# Isolate Configuration


# From https://www.ucw.cz/moe/isolate.1.html

# Default runtime limit for every program (in seconds). Decimal numbers are allowed.
# Time in which the OS assigns the processor to different tasks is not counted.
CPU_TIME_LIMIT = 5

# Maximum custom CPU_TIME_LIMIT.
MAX_CPU_TIME_LIMIT = 15

# When a time limit is exceeded, wait for extra time (in seconds), before
# killing the program. This has the advantage that the real execution time
# is reported, even though it slightly exceeds the limit.
CPU_EXTRA_TIME = 1

# Maximum custom CPU_EXTRA_TIME.
MAX_CPU_EXTRA_TIME = 5

# Limit wall-clock time in seconds. Decimal numbers are allowed.
# This clock measures the time from the start of the program to its exit,
# so it does not stop when the program has lost the CPU or when it is waiting
# for an external event. We recommend to use CPU_TIME_LIMIT as the main limit,
# but set WALL_TIME_LIMIT to a much higher value as a precaution against
# sleeping programs.
WALL_TIME_LIMIT = 10

# Maximum custom WALL_TIME_LIMIT.
MAX_WALL_TIME_LIMIT = 20

# Limit address space of the program in kilobytes.
MEMORY_LIMIT = 128000

# Maximum custom MEMORY_LIMIT.
MAX_MEMORY_LIMIT = 512000

# Limit process stack in kilobytes.
STACK_LIMIT = 64000

# Maximum custom STACK_LIMIT.
MAX_STACK_LIMIT = 128000

# Maximum number of processes and/or threads program can create.
MAX_PROCESSES_AND_OR_THREADS = 60

# Maximum custom MAX_PROCESSES_AND_OR_THREADS.
MAX_MAX_PROCESSES_AND_OR_THREADS = 120

# If true then CPU_TIME_LIMIT will be used as per process and thread.
# Default: false, i.e. CPU_TIME_LIMIT is set as a total limit for all processes and threads.
ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT = False

# If false, user won't be able to set ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT.
ALLOW_ENABLE_PER_PROCESS_AND_THREAD_TIME_LIMIT = True

# If true then MEMORY_LIMIT will be used as per process and thread.
# Default: false, i.e. MEMORY_LIMIT is set as a total limit for all processes and threads.
ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT = False

# If false, user won't be able to set ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT.
ALLOW_ENABLE_PER_PROCESS_AND_THREAD_MEMORY_LIMIT = True

# Limit size of files created (or modified) by the program in kilobytes.
MAX_FILE_SIZE = 1024

# Maximum custom MAX_FILE_SIZE.MAX_MAX_FILE_SIZE = 4096

# Run each program this many times and take average of time and memory.
# Default: 1
NUMBER_OF_RUNS = 1

# Maximum custom NUMBER_OF_RUNS.
MAX_NUMBER_OF_RUNS = 20

# Redirect stderr to stdout.
REDIRECT_STDERR_TO_STDOUT = False

# Maximum total size (in kilobytes) of extracted files from additional files archive.
# Default: 10240, i.e. maximum of 10MB in total can be extracted.
MAX_EXTRACT_SIZE = 10240

# If false, user won't be able to set ENABLE_NETWORK.
# Default: true, i.e. allow user to permit or deny network calls from the submission.
ALLOW_ENABLE_NETWORK = True

# If true submission will by default be able to do network calls.
# Default: false, i.e. programs cannot do network calls.
ENABLE_NETWORK = False