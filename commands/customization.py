def stand_block(msg):
    return '```' + msg + '```'


def frm_ls_to_block(ls):
    result = '```\n'
    for i in ls:
        result += str(i) + '\n'
    result += '```'
    return result


