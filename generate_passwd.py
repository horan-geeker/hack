def personal():
    file = open('zpjyyyymmdd.list', 'w')
    prefix = '201'
    endfix = 'zpj'
    for year in range(4, 8):
        for mouth in range(0, 13):
            # for mouth_end in range(0, 10):
            if mouth < 10:
                mouth = '0' + str(mouth)
            for day in range(0,32):
                if day < 10:
                    day = '0' + str(day)
                file.write(prefix + str(year) + str(mouth) + str(day) + endfix + '\n')
    file.close()

def xian_phone(personal_prefix='', personal_end=''):
    file = open('zpj-phone.list', 'w')
    prefix = '8221'
    for num in range(0, 10000):
        file.write(personal_prefix + prefix + str(num).zfill(4) + personal_end + '\n')
    file.close()

if __name__ == '__main__':
    xian_phone('', 'zpj')