import re
import requests


# check for email format
def check_email_regex(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # returns True or False automatically
    return bool(re.fullmatch(pattern, email))


def adobe_check(e):
    # checks if email is valid first
    if not (check_email_regex(e)):
        return False

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://auth.services.adobe.com',
        'priority': 'u=1, i',
        'referer': 'https://auth.services.adobe.com/',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'x-debug-id': '3da3bc8a-709b-4278-9be5-25feee481e44',
        'x-identity-verification-token': 'eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiY3R5IjoiSldUIn0.bsDVszrvXvWEw6WQxjLdKl9RgGZCqS546jJTjmMRDqTqBWiOn3_TncNvlK4z5u4lD-mtUnhu0kmWZjT7bIcLiID856BBfboUh3jftIda9c-Fyreyczy6bHtKM-mCbr6hIij4s5jrvcU06UZBstLSAGfChmhgg6fhkA1itoBNDMM5UQuiB3eCN62j9s61zxzqzhJ6Rq_R8q2rG_J0z1hwD2ESLwysSPEfck7Gc1jcp4y7pA70Le6ret_w-y63sn-HzfDanUZDigknLd3ld6F5-ifY_Duyvkr2ViNec7wo07c_s7tW5Rjb-ZT0yJpqJ5ghLBXNrQRm_RTS1RLQwYZs1Q.TcQww-BhvTepBi6-3qZ-jg.XXMixgArFcx4JjzIxiFxwg2wdukktr2QBrS8RgF8XD6ZOyM1VWjOxpGCfksXzKiNaxNXoLd7GbffzKdcjMtHR1TU3AVpGHWn9UwPTY_1L8lIqhBkqmprCu2V1pMWB_CCHo0oNkttC9zjm9aPvMWrgAExLuKHgPf_-gNs7yqvpUTo88O-eEsGQpneq-69tr0hOdw0jxcUyUcFMUCscNLXET_l_Tx_U7Ap6MFTKtWCfoVrbiwTv6FEJnEmfCUiBq6f8w6ZirBdH_T69KNGl_hOAbFwJd8BRkhrFkdbhM-V6gjRfj0G7Cw8XpbOOMALlnjZ3kM9fRN9lB0jXOgIn1IW9-C39sjnlEd-uityzra6yEcYyzX0eMAv3p9yUxDZgQP3rjbB4P6K8ReHjrjcUnsirRUWwxKS0VatCDfM-i699CDeQURCqNMDONUgMs3bQMVCXnX3AT8NgdJA2uwdMYDPoEs29dgMf3WZcSDcrsMmyvdJETzBeuEiyPZAQnP4Q20EyyFwqlLhtutAVxxSo4UKmBGnpGMre49DIaKbyxK_F2Yw5yO1l4hcIHlisRn2Jh0v7P_A2kyVh1EPMqrV23oHZGR11_BY4dDW-VY9XxXMspaU7i_5uX8zkJZYFL_mqH7vjrApjYkKjZevbSUBHZELMBrm99KjM8b2kwOID3qL82r3nf7xbOiCRvQr6E6-qsgRq4UcEWXhN8xfFBj4JVIrG1EsTz0cguiPk1fzz1lirRg1gBaaWVdaWTFIbaYBd9GVAb2ybwEDnDBF7qdMP8ZDaFT5_3FUc_pXS_X2fd-sv5ekHXgebTmvoOXKti1etpU08d88ATsIJWp41lGBSto8wqaNM-QS5W7RotOuseUU1iyljcPcoXuE8cfFK5i1ZKlIEs1aVmsbanS7C29onEZKar76MUhstIPBG6v7KiHgIS7UtRuunDPz-a4R4x_EOyUBErCDhKmrTygngbUcQ8A93vdCDELiWQ98AQbuH5dm2QitbMQogz1JQyHQ-LaM1PsVvtzMy95Zwb6G4ffjBB-c4FOwHwazP-ulCBnHJtLMtWftf98zvvPDVnPbhf88Hl8DbBNAKZQejQDzcOIBHe8CZ_tXG0VdgtoAHuWNohxSK38kGl4_T3QmLhsOZ7Zs8CfaGD2UZNk__fSrBHwQwQXusAXl6WCKQWmzSDrCv5fIsevvrCmIvmhK0PgT6c9G-jQGQFU4vj6dCvIOc78gAeodD8VwO7sCPKl5ONLKrz4OHwsUCctyiV_hpQe_-HETDEPdAt-T48mccHjsj51fqLerLlmmlxKJEoaRHACPLuELUbSujREYcB7H3qcJyfFVAcI6w7Y5ieRjHSeEMe5rn14t4rJWQkZOoAROIBPXRjXSKOSgKuclV2-oPKlGO1ssnO7RaV7ejwFcudQKGOQhkEFDW562sp2sanUweYyyl3w5oihYwpGTRd1njgZwolJJK-XndJYZSoRFr_isgskk7DW9uJqeHw_eDERqiewni9Cr5zwkDDRgbytePOjPglhmPQEpYasGcEJAb3NnSm_u3liG1hP_7zF33Aj4HIZYpuMY0qoyQP42XsJKC74ijyZx6FjpD4m9plR283CmQaviknNcLvVJqieBEeB05OFSLrC_ypz87ZxIB79SPlRsNr8rMkeWm0MOuG6sEy9G05mNBpN4eyKyB4SzpUS8uIGJwnLVWnjfngreHK4TDXYrqbtXWlnZ.-JhNuUI2t1BcHJRPB-TzuJO2Xx2W-M8ALluzoKZZpeM',
        'x-ims-clientid': 'SunbreakWebUI1',
        # 'cookie': 'OptanonAlertBoxClosed=2026-02-11T23:56:48.161Z; OptanonConsent=groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=MCMID|23371642200315182810571007460907837944; adcloud={%22_les_v%22:%22c%2Cy%2Cadobe.com%2C1770856013%22}; _uetvid=5717e97007a511f188be3bb698e76c8a; ak_bmsc=DFC547024FACFCE036453D431AF5A061~000000000000000000000000000000~YAAQ5FQhFxcgRx+dAQAA3BAVRh/wodk/HQAb/myBvYYn3vLcNb+va6DSgd9/srT1tlPxS4+4v1ZzyFWLdZTxg4mGlwG5NFAtlrRNc8DsTV8h8Hu26SI6OBGgHgl6RE3dVQi11G9HKF1W6iqgAEGVROJLRi8KApGiKVBlwTq6f6sc+i8WHQGud+/cJqy7LfNYhqgqxbLPDDtOGjToFDz2J/r4xdWhxyDUzNlNi0Rhn6ogO1XRCzyn+bbG8bWYAbnlyAGDuYn+Nu+bcLD0iaLrYLozjKw/sO/8gHYmEnVsJ1Bcyq/ozz9NmOCW2zTz8MEZSSTzIdLki2VUgjqYL4xtMe9FjxVufgzJZcDNKUfCwBOxiCx/BJmeU/skHr0gkdXmef3ldC3tokUTwg==; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_cluster=va6; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_identity=CiYyMzM3MTY0MjIwMDMxNTE4MjgxMDU3MTAwNzQ2MDkwNzgzNzk0NFISCMWri%5FnEMxABGAEqA1ZBNjAA8AHxpdSw1DM%3D; s_nr=1774997280914-Repeat; fg=2KTJRM2GFLM5ADEKFAQVIHAACI======; mbox=session%2323371642200315182810571007460907837944%2DaBslbx%231774999141; mboxEdgeCluster=34; relay=3da3bc8a-709b-4278-9be5-25feee481e44; ftrset=258; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_consent=general%3Din; gpv=Account:IMS:SimpleEmailPage:OnLoad',
    }

    json_data = {
        'username': e,
        'usernameType': 'EMAIL',
    }

    try:
        response = requests.post(
            'https://auth.services.adobe.com/signin/v2/users/accounts',
            headers=headers,
            json=json_data,
            timeout=5
        )

        content = response.json()

        if content:
            return True
        else:
            return False

    except Exception as err:
        return False
