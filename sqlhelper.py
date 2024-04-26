# SQL module

import psycopg

def get_ls_from_db(adrs):
    """Get's adress string connect to DB and use address to find LS number"""
    split_adrs = adrs.split(',')

    ls_result = ''

    q = '''select * from ls_adr_split a
    where a.str ~* %s
    and house ~* %s
    and kv = %s
    '''

    p_street = split_adrs[0]
    p_house = split_adrs[1].strip()
    kv = split_adrs[2].strip()
    
    with psycopg.connect('dbname=adol_sah user=postgres host=localhost password=123')as conn:
        with conn.cursor() as cur:
            cur.execute(q, (p_street,('^' + p_house + '$'),kv,))
            b = cur.fetchall()
            cnt = cur.description
            #print(cnt[0].name)
            for record in b:
                #print(record[1])
                ls_result = record[1] + ' - Это номер ЛС МУП САХ, относящийся к адресу: ' + record[3] 
            conn.commit()
    return ls_result
