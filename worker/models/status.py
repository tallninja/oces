# SIGSEGV:  Segmentation Fault                      11
# SIGXFSZ:  File Size Exceeded                      25
# SIGFPE:   Division By Zero                        8
# SIGABRT:  Program Aboorting Due to Fatal Error    6
# NZEC:     Non Zero Exit Code


class Status:
    queue = {
        'id': 1,
        'name': 'In Queue'
    }
    procesing = {
        'id': 2,
        'name': 'Processing'
    }
    accepted = {
        'id': 3,
        'name': 'Accepted'
    }
    tle = {
        'id': 4,
        'name': 'Time Limit Exceeded'
    }
    ce = {
        'id': 5,
        'name': 'Compilation Error'
    }
    sigsegv = {
        'id': 6,
        'name': 'Runtime Error (SIGSEGV)'
    }
    sigxfsz = {
        'id': 7,
        'name': 'Runtime Error (SIGXFSZ)'
    }
    sigfpe = {
        'id': 8,
        'name': 'Runtime Error (SIGFPE)'
    }
    sigabrt = {
        'id': 9,
        'name': 'Runtime Error (SIGABRT)'
    }
    nzec = {
        'id': 10,
        'name': 'Runtime Error (NZEC)'
    }
    other = {
        'id': 11,
        'name': 'Runtime Error (OTHER)'
    }
    boxerr = {
        'id': 12,
        'name': 'Internal Error'
    }
    execerr = {
        'id': 13,
        'name': 'Execution Format Error'
    }

    def retocs(code):
        '''Converts Runtime Error to Status Code'''
        if code == 6:
            return Status.sigabrt
        elif code == 8:
            return Status.sigfpe
        elif code == 11:
            return Status.sigsegv
        elif code == 25:
            return Status.sigxfsz
        else:
            return Status.other
