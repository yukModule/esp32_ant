config_dict = {}

def read_config():
    '''* 读取config.txt并生成设置字典'''
    global config_dict
    with open("config.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            cmd_p=line.split()
            try:
                config_dict[cmd_p[0]]=cmd_p[1]
            except:
                pass

def get_config_var():
    '''* 获取设置信息'''
    global config_dict
    return config_dict

def save_():
    global config_dict
    lst_new_config=[]
    for key,value in config_dict.items():
        lst_new_config.append(key+' '+value+'\n')
    print(lst_new_config)
    with open('config.txt', 'w') as f:
        for i in lst_new_config:
            f.write(i)

read_config()