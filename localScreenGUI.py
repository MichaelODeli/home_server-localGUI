import logging
logging.basicConfig(format = u'%(levelname)-s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'home-server.log')
logging.info(' ')
logging.info('App launched.')
logging.info('Logging module imported.')
try:
    import PySimpleGUI as sg
    import psutil
    import traceback
    import os
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    import vlc
    import datetime
    import pymsgbox as pymsg
    from sys import platform as PLATFORM
    import fileManager as fman
    import fileSearch
    logging.info('Other modules imported.')

    iconHome = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAABGklEQVRYw+2TvRGCQBSEISAjpgFKoAZDxxlnTCAjJSOyAiILsAAzO3DoQDqgAEkl0oBZ7zlzJ4eiHD8GersJ8vDb6DMMHZ2vBiY2rOZUeAs7UHawpsDbOIDnAHtsvIMM9WRwxsS7yNFMDncsvIdCYI+sPAW8MfAzlAKZYsmait8lZkPxPq4Ct8cCc9YFe+K5wh+Cj1EJ1PYO592K9xXi/lI9IImEpya1cXX5hFSUC9ZPeOqaXXjU5JOkOiN6iadG7KounyTVCWErnhqyL9Tkk6TKEbzFUwPpe1dFKmD1EU9d1f7xXj5JKsq8Y+tpl0+Sqv9Am3ySVMMGPsv3NNCWxr27B3qg70DXux7QAz810EjXux4YPqCj82e5ASnAWRYMdgfqAAAAAElFTkSuQmCC'
    iconCPU = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAfElEQVRYw+2WsQ3AIAwE2YOZMqZHg4odPg1VJCe2hVGQ/qgQElfYmC+FkC1gou0pyBCgQtBhpUNQfdcPeBkOBQQRxC5oIUFzFxWXcXmLTsH3xU+BhnJOQVygFlkZduu6iAK26QHvgON6vyD900+PLdnBKz06Mr7/T0DIKzefCDRb+h01/QAAAABJRU5ErkJggg=='
    iconSettings = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAACtUlEQVRYw+2Xu08UURTGNyGhpIEQwp9Bs9ZUJHJYVuSxCoYGMWiicUtCggEVjBqkAA1mky1I+BcoaLbSxNgQQGh5qg3LU8iSnwVnLndgZpZdZwoTzjRz73zn++7cxznnxmI39p8Y81y2+TDpq/Gy6vAE4p4C8fAEuj0FusMTGFbKaQThs7aGwxOYVcohBGFUW7PlkTWyyRyNpl3FIHml7EcQnmorzyBVlt8cmxd+fvSVrKr7KmlqaGXbmvV2BHGtyA5JakhbXpXBAmnXMp66WnkEQWjhTwAqHURfyy7etsMUKRUQ7vOJ3z7IXWr9BWYUdMCx5XLEWxKG3HmSfHD9ySF7+jbjR9/AmUJe0s4YawAs0nOF3Hl6+aGYUZK8Vu8zGrwFcgpYMuMdYMK895JhhX32WSFDr/beYZI+fU+wogw5L/om87NfdbdcPAmyFFwzXSB7Zdo6+W6+N10VuMWJ+byhO96hz3kuZ84l8ZAt8+XEM04RZ92CjBjXLH6WNZgX1vDWfcMgtSxY7s917gvGMUUddaTMQAq6Fs8sr4WAbRqLUcG4gT5CEDKGvtrKD45EBkHoMz7jVBSPRo7z+cFadlouTEp7lxGEDmcQ1wt3RwpvRRBzfOpdmHrt3UMQbjtHsjSBlmsLNJcm4ExRVwRTFPEiX9qm6ZC3qeugnTIW8kEjbkG2GCg5VPSxERgqrGD3jc6ygt1dvgQEOytcL+oGFfqZJBkYrhNM8MSk0qWAcO1KOCO08UrhSzzwTTg9LAKwxhs6TDnjl3CslJk3hw3gmPd6qt3T9u4S6qBIygxM+r+Y5p4h72KKn2Uk/SJly6HSN5tCrNSyxaPwSrJjOZ/H1zarZ5vWkgqvIqXjY1dgKKd0LFL8DiMIQ/9U/AaW7x8RhOnwy/fILyCRX6GivgRGfo29sUjtL+HgQz5j/Z6CAAAAAElFTkSuQmCC'
    iconTorrent = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAACQ0lEQVRYw+2WzWsTQRiHhxoRRL2KUvxTvKggyMQ2MXrIoYdYC7EiivXmRVtSBRW3CloEqbVSBE/iH+DBi2cLIT0UqaR+oGhLlVjt42En72433dnJx3F/c9mPd57f7LzvzKxSqVKlchIZjnOHtyyxwTpLvGGSI+zqDXwP11hhO60wxr5u8QN8xqZPnOgc3oeHi+7R1wl+B89DkG/McYUiWQYocpU5fobePunAgtvSvcEUOXSk5bnPH4m52y4+J12XKbXAm+0syyZqs61csJePgi/G4jWaIh+kpna7oPdziZcyrgbDVrxGM0zDRF9Ohj+VYF8PE/EazQMTXSdjw5/ie6T8vpJ3Msjzw/Q4HI8v8y+C/8KEE16jmTd9KvHrdVPA76lQ4uQ2mLrE1CNvxszzdd7xiGORVcEhmZxfjJONHWe8QSHy9VWOhg0em8e/OW+diHgDLWUd6How/uZ6vJEw0zaDeUl0oEnf4IK5XUhMpc3Ab2e4yAv+yurOKqV4bW4nemDgt3OyxS+SUdTMzVBMuH3L9hJW92nFqrkcjB2R1yZeo5k1Ec8Cg5zlo7028ZoRE1NTVBOmKM7Cs8Y3t/vVIMmVhBR7beC3GJSdy9RzxgdTVFX0s+FcqJ4jXjMjSVaKaTleRh0sXPAlKdOCUoqD8ofQYNx5i7bh67LQdvrbhQ6dBgtUGLIWrS21I8yETsXBYEcdbTlwutetraeCliXXG91s+RnjANNSUd1pMTQ5EZN+yryixlpH4DVqzFIwqU2VKpXRf66Kl73fyrorAAAAAElFTkSuQmCC'
    iconSearch = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAABQElEQVRYw+2WO27CQBCGt6AEydRJa1GkpEvhy8AZcMTzAknly6x4iWMAisQdsCgowpci9sQoEGcNY6Xw31j2/jvfzs56d42pVElV+IRYtsTEbLGE+PcL3mbBJS1o3x68RsSJazoRUbslfJMleVrSLD76bPgZHXzq1PHpMDtDFMuCSEJsCH60BmykPSpW2nTuV3gXHR4rqYV7uZnL6L2rHk+ymLuGb0n6wa++QHwtN0Av6TbNdU4TZ88NkK6Sbq6zm64yN8D6r4nLZK7dAPukWyPX2Uice21ArD1F7/+syO7LNNT+0Z50twqru9l98Ky7Xb/qHjhHHjWPzGPynOgc+m88yNv43tcW+1XazJeiiLOL14Edlpfvdc8kgxjp3PvG5SKGOohRuYiBDmJYLqKvgxgoAwShFd4YY+irhq9USU+fTvn7Yv4/rEAAAAAASUVORK5CYII='
    # original # iconUnlock = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAABBUlEQVRYw+2WMQ6CQBBFjYmdnsBDUMIlLCgoOJJ2egWl5jpESgI2VNrQPZuFiKKuu4yJcT8dP/kPZphlJpM/ETMi9hy5cOHInojZmPEhOffKCccJn7LmmdZM7QEbXmljX5xWDVsC5swJ2NJ090O71ra1L/B6jkfR9cK83UTd03sPnte9RWQOOKiI3aC7U+7BHJCpCH/Q9ZWbmQPOKmIx6C6Ue5abbyUHGBvAkoSKT1WRsNSLrzFVrYEgwUbJe0BpBSi1G8fqw0u34Q7w34CYlBMnUmIJQHwz4fUAwhqQ9gYqHR9Q3R1tvwcQL5F4k8U/U3dUOIA+QPynL762SC9e4quj09d1BbHpvGF60ytxAAAAAElFTkSuQmCC'
    iconUnlock = b'iVBORw0KGgoAAAANSUhEUgAAADoAAAA6CAQAAABLsoKjAAAABGdBTUEAALGPC/xhBQAAAAJiS0dEAP+Hj8y/AAAAB3RJTUUH5gIJDzoEIpkTiAAAA6ZJREFUWMPtmN9rk2cUxz9vfpgf/qgjdW0vJKzqjAt0MFcW6H7hRcHuP3DCYOi/4aWX+xMGu9FrxSkIU9Ahm9DhMqSdMmuJYCK6tpI1aV7zfnfRZ1nSvvZ53zeNDtzJTXhycj7POec55/kBr0Gc4KraNlOBNTvIPEcYZ4QssEqNB8yxGM5YID0DjJPnAz7ifQ4waqBV/uBXfuYXFmmHDJ0NKpTRpM5qQZ42iqcFndWkMrKmIAwQJTStC1rzQa5j13RB00qsa28XdEaX1OyCeGqrLa9rEk1d0kwwaMKGBGIU+JJjpMzgXW5Q5gnwNhN8ShGAFMdY4SHzeOovs0IopTOqGH/qOqeTKmq3ENqtok7qnOrm14rOKNV3gIUSOqxbJox1ndekYqLrE9Okzhusp1s6rET/0CGdNn66mtVRJbs9EUJJHdWsXOPraQ3ZoDErN0uJXQBUuch93O5adABc7nORKgC7KJG1mbRD0xTIAFDjGg1fnQbXqAGQoUC6f2iSvFm3Te7R3thzHIA293hutEdsFWEtGeAZ37AHSPA7f+L56ngs0TJO7LE7EgxqF7ezupL2IrVAgxS5g0L2eXtOByA+nkYqba/zN+H12tgchE0jRn0vx5lghHTAOTh8zhgALa6yQosaZa6w7Afxh+7nK76gwN4+YrjMPN/zHZUACRfK6ZSWtR2yrFPKbQ6V30IqcIKdffj4r+zkBIXNw34lk6NIHID2+rkngsSJA3GK5IJBs+wzafiByyQjIF1mmAYc9vm1fz9orJP5J/zGjgjQFh+ab45fArfuSHGSkTyVSc9L5LV0pDcHat/a/ESm1zpdi27AUDFKgVGgyjzV8Ngo0PcoMcEY8JgyPzE3aKjDMMf5zHh3gHHe4ilPw+2HYRdSjBIHe86gBymFtRJOXcQ4xHDP2DCHiA3WU0htSEmic7EaGFTUqPeM1KmFPeGEgzp43OFRz9gj7uCFK5uwq9ejzDsMkSMFrPGMWcovOYJvGxRecJkFPmYceMCPzPEirIkozaHBXR6yA2jxF2vhDUTrvU1WzbdX1nvB2XqTtsmbs5/+Bzdx4YWtQaD7OhUY2qJBGgeYYixSLDzGzaSb5oZuhT5nkXdxgDz5KOHritSieYvoET8/KlzH7Qv2j7hcpxJockpoSre1ZJ6jooqrJd3WlN/7mf/9NMMRvuYT9pONdDF3WKXCTb5ljkbQSzEkGWOINPGI0DZNVni8niYrNOKbw5Yz+F9eqfwNTQ86LlK7J2QAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjItMDItMDlUMTU6NTc6NTcrMDA6MDAV73LpAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIyLTAyLTA5VDE1OjU3OjU3KzAwOjAwZLLKVQAAAABJRU5ErkJggg=='
    # original # iconLock = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAABBklEQVRYw+2WPw6CMByFDYmbnsBDMOolHBgYOBJucAXozHUMjkZYmGBh+1wq8Q9qbamJsY+Nl7wPfo+WzmZ/IuaEZJR0dJRkhMynjA84cK8DwTThHjHPFOOZA3a80s58OBf1JGxYsGBDQj/cD8yqvcz+iH/j+ByHLvTrJhye3n/w/OEtQn1ALiPSUTeVbq4P2MuI9ai7lu5eH9DKiOWou5Ruqw+Q0vUdQBfACkHFp6oQrNTiG3TVKCAQmEi8B5yMACflYtl+eKkW7gD/DYgoqKkpiGwAoqsV3owgjAHFzYIqpgdUd1vb7wGsj8h6ydY/U7dVOIA6wPpP3/qxxfbBy/rR0enrOgNr3NxBx5uCcAAAAABJRU5ErkJggg=='
    iconLock = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAQAAAAm93DmAAAABGdBTUEAALGPC/xhBQAAAAJiS0dEAP+Hj8y/AAAAB3RJTUUH5gIJDzQ55HJyFwAAAkNJREFUSMfVlj1r21AUhh/ZcowXG1qTIRhKCknqoRgKSclW6NJupskPKWQP5B907ZAxQzKUbO1SaKbipZAE4oKhUDDBseuCbUhwbOnt4I/KH9KVqJe+i7m65zw+es+RriwCJJ/rVkBOwN4QZ/OYHGmgTZUf9IPTLAOuwBte8ISHQJPvfOED56Yq5+KE4tpRSY68clTSjuLytcMfh3ZVGUI6aqqpzhBe0e4gIhqwoJIkqa1jFbWqVRV1rLYkqaRCVKCtAzmS2tpXRqOaM9pXW5KjA9nRgOs6k+ToZIAb153RiRxJZ1qfD4z5MHNsALcc0Rp11AJoccQtsEGOSMA0WeCeC++AWAAX3ANZ0tGACeKAS2dmp4MLxElEA5rn1ifC9i48NveHv72ZJ7r3N2K042VbU7gUr3nJAx6xDXT5RHeqhCSvSAJf+clvPvORO59yhZa0pxtF0Y32tOQzkUKbuoqEk6QrbXqBEx6ywhrQ49vYqSAleEaCNVZ8m0ISG7jjHS1jn0WG9ySwSfoDR4r7XJ+OmqNYiMRIClMJuLhALMzfhwGKZXJAlYb5CTIDxVOK5IEyp1yakCagyzJFtgDYAmrUg2/c5IpLjvx4lSeHG5yw8C6bgDGqlMerMlVThsnDGA1OYdyUxr8CweKS2iLHBizq1FjgYIdEjUIXrPkVOvRDvL4cM7BLH5sUb0O+YFNAf/LUmQReUyFPgucR7rHCtXc56eE5h9QjWVbncPABOtL8YzQbEvdr9hidsD7SV+n8qv4D/QHmmWR4e1ewJwAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMi0wOVQxNTo1Mjo0OSswMDowMG9Twm4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDItMDlUMTU6NTI6NDkrMDA6MDAeDnrSAAAAAElFTkSuQmCC'
    iconRam = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwAQAAAAB/ecQqAAAAAnRSTlMAAHaTzTgAAAAbSURBVHgBYyAX8P8Hgg9wih8nhapyaJtJGAAAzw5sSb0+xTcAAAAASUVORK5CYII='
    iconMusic = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAABWklEQVRYw+2UvYrCQBSFBbFTUCxtJa9gYaX9Fvb6KnkGn0CwSKFvYBFT2WkpiGCplZWWAb8t9u46Ls5kMgZBmJMy59zvzs+dUsnL6y2iwYgJCXuuXNmTMGFEo5jiA2JSniklZvBa8S4rsrSi61a8zBhbjSnnLV9n8VBiTUifNlWqtOkTsn74v6Cer/xWCc8InroCZopra42grHR/oGP0djgoq7DbKGXvlzQz3U2W97Owuzn38hWrhioKIvtG/V3MQ3b3yip+N2qVPVY/upn3/slZ3CRpHj1isc1zz81ckrH5zUml/yA3IJA1pIY3iqF0sXGa/Y2kh3rLVCyhEyCU9FRvScTScwL0JJ3oLTuxBE6AQNI7veUilpoToCbpi94iKjkqM/82wH8V5feAHIAv+WwBln4P8ICPABwLGbSjHhAVAoj0gBbnlwFnWqYXvUXEyRlwIjKW9/Jy0je5PKzzo6moagAAAABJRU5ErkJggg=='
    iconVideo = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAsUlEQVRYw+3WvQ2DMBAFYNaIWIYFPAeslcJrQEZJA02YIPy8NCiyOWwJ/FJA7tHdSffpFUjOMo1G4wQ5LDoAQOFMG2DXbIk8f8Pru22cebFzFgTu3j65gwSeHpDcQQJvv2JqhzBQczqEgYrTQQLDsjGcDjGgBCExwKx/Gj5Q/RowePCB0QOOfwocByYFrg/MClwfwOmBFsy0ErBUwG69rXva+R55/Pmekg5287xG88f5AEpKc9/QhzxgAAAAAElFTkSuQmCC'
    iconLife = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAB4UlEQVRYw+2Xvy+DURSGr0FiYhAjoxgN/gSb1KcDKVNj6CYmKYuBRTTVhJGwdJcIicVgsRBSWyOxGKQxsEjatPFYzndS/eHe23ZQ6Xume3ru+3w9ue09nzE9dZEYYZUHHlhlpNPW/QScUiJUiVMC+jtjPkmGAo1UIMNk+y2xqZWW1bUkVJ40afJ1eZ+WNWnJO1kSRCQSZHlvsWV12ypcsU5UzcOIss4VldpyP0CeNLE66+qI1bbMHVDdElskyPoDIp7RDYBq9QD/CmDT3wMUpTLwAgSyKtoBL1Ia8wLEZPViB9xL6bIXYFlW93bApZSueQHWZHVpB6Sk9NDrmB5JPmUHzEjprRfgTvIzdsCQ3FIVFp0BS7pnyOVWvhGTfWfAgWRv3K79eHjk9LfwOyDQox13AwzwJht2nK6aXal+Y8B1LtrRYWXear/AR/g47oPXsH6Hc4v9LBf6/MM+s11cu733KyCjdXHjI/q41sEr2dR+Qweva/p859MxXhWx1dB+W+1fGTP+YopPbcBxzfAY5UQ/+2TKtCbmKKvNMytqv8Kz5svMmdbF9I8pOscmm+R+TN3Tpj0xwVPTv+onJkz7YpBUg5eREikGTafEOGd8qfkXZ4ybTotRkjzySJJR01MX6RsEXMucr5f1XQAAAABJRU5ErkJggg=='
    # original # iconExit = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAsElEQVRYw+3XvRHCMAyGYe0BY/CzGp2mSTZLKriwwUvDcUdhGywpgTt9vfMUUmRZJJNxDntGZnozM7Crf/6GNdcKwYhHhjIwuQBTGXimu4Kt8wmYARQNBFCAGmECuLzaUGOAA0uLMNaQY4uwNkmTMAMinLiXCQdAhHOZ+LjIX0SjgTfiLwH9rSJv3qbBP5rDqAgfdpuO6/ALZ4UrM9eWVYDw5Td8fY9+gIQ/oTKZrjwAm/oCnITJuaYAAAAASUVORK5CYII='
    iconExit = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAQAAAAm93DmAAAABGdBTUEAALGPC/xhBQAAAAJiS0dEAP+Hj8y/AAAAB3RJTUUH5gIJDzYwr5ioMQAAAehJREFUSMfllr1OG0EUhb/1zyIBCRFYKIIyfoJUkRHPkC6p4Q2oEFVChRAFDRJKE9dJirxDFlymj0QbKSIg8eMU9uIcCi+Z9YztGVubirPNanb3m3vvuTsz8OgUPdyoIFA0gCszT8VMEiBxR5ueQVVyD+d4ywZ1qsHhRqSc8ZHP/HEmUlmbutE0utGGynKAC0qmwknSNy08AE3KFV4AcEhCNTDllHW2gLrhGGBEDEDC14ns3QJiY2TelH7UVSybTXVs+0WWS66AJV8AAnhOPTRgD1AAq7zjmLWw5s+nPLyhl9lhk5hZtjnRyNfcCP9yySXXdKw3utm0DfZpWAUbl5pKWlRNNc1ocBytqqlUknSihtA/pNAbSdJv1dzGzl3OuEEmfeSEwCHXsj6ok49yFNCY8oRDno4skFjJ3FjjoG/PWHOEaroO/ncTvdSICL2NPalMyh2+eFJ+lf1oLXb47uEWZ8p/bJvCG3tRP3ShK722gM90pJ4k6XQQ5+vDEkssATNWeWPgjpgW27TAtzi4C6ytc/YoU+c9pz6YDRyiCMFPdpnnLATnBWbIXwGkIcB+ACljuttRmvvSAoouAOsw0TYK0HXmKm6jN4tDmya34bXK6ZYmbTflHp9g6sNSb9CIAo9zhR84H6HuAbCGTEdCaLm7AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIyLTAyLTA5VDE1OjU0OjQ0KzAwOjAwA5rT6QAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMi0wMi0wOVQxNTo1NDo0NCswMDowMHLHa1UAAAAASUVORK5CYII='
    iconSubs = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAwklEQVRYw+2WsQ3CMBBFs0dmQiBBQypEi2ABNoAFyAAuEBvQMANMAEVSOS1KEfQYgEQosr8I0j33fpLv/p2TxBgs9MQE8QXG//R/72KbwJps2AlIcZShRabEkbZf74mFb1HgiIn7FBRRBUV3wEaBpytwXwVrtQAuLLUCeHEiUwoAanJmSgFAxZ6JUgDwYKsVANzYaAVXpeCufCLPjrGqyE8OTFVt2nBkrgvamYVyVKzUwy54XMsXjnxlqpe+/Nti/Iw3Jof1QhWrfUAAAAAASUVORK5CYII='

    DarkGrey14E={"BACKGROUND": "#24292e", "TEXT": "#fafbfc", "INPUT": "#1d2125", "TEXT_INPUT": "#fafbfc", "SCROLL": "#1d2125",
                    "BUTTON": ("#fafbfc", "#0a0f14"), "PROGRESS": ("#155398", "#1d2125"), "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0, }
    sg.theme_add_new('DarkGrey14Edit', DarkGrey14E)
    sg.theme('DarkGray14Edit')
    logging.info('Icons and theme created.')
    mainLayout = [
        [sg.Text('Main page')],
        [sg.Text('+ Stats')],
        [sg.Text('- Settings')],
        [sg.Text('- Torrents')],
        [sg.Text('- Search')],
        [sg.Text('- Music')],
        [sg.Text('+ Video (to-do - id play)')],
        [sg.Text('- Life')],
        [sg.Text('- Subscriptions')],
    ]

    systemStatsLayout = [
        [sg.Text('System stats')],
        [sg.Image(data=iconCPU), sg.Text('CPU load'), sg.Text('0%', key='-stats_cpu_load')],
        [sg.Image(data=iconCPU), sg.Text('CPU temp'), sg.Text('0°', key='-stats_cpu_temp')],
        [sg.Image(data=iconRam), sg.Text('RAM free  '), sg.Text('0GB', key='-stats_mem_free')],
        [sg.Image(data=iconRam), sg.Text('RAM full    '), sg.Text('0GB', key='-stats_mem_full')],
        [sg.Image(data=iconRam), sg.Text('RAM usage'), sg.Text('0%', key='-stats_mem_usage')],
        [sg.Button('Reload stats', key='-stats-reload')]
    ]

    settingsLineOne = [
        [sg.Button('Restart app', expand_x=True, key='-settings-restart-app')],
        [sg.Button('Reboot system', expand_x=True, key='-settings-reboot-system')],
        [sg.Text('Cooling mode'), sg.Button('Silent', expand_x=True, key='-settings-cooling-silent'), sg.Button('Standart', expand_x=True, key='-settings-cooling-standart'), sg.Button('Turbo', expand_x=True, key='-settings-cooling-turbo')],
    ]

    settingsLineTwo = [
        [sg.Button('Exit app', expand_x=True, key='-exit-app-settings')],
        [sg.Button('Shutdown system', expand_x=True, key='-settings-shutdown-system')],
        [sg.Button('ON/OFF Wi-Fi', expand_x=True, key='-settings-wifi'), sg.Button('ON/OFF Bluetooth', expand_x=True, key='-settings-bt')],
    ]

    settingsLayout = [
        [sg.Text('System settings')],
        [sg.Column(settingsLineOne, expand_x=True, expand_y=True, vertical_scroll_only=True), sg.Column(settingsLineTwo, expand_x=True, expand_y=True, vertical_scroll_only=True)]
    ]


    searchTable = [
        # ['youtube', 'y3', 'Сосед_Комкиных', 'ТОКСИК-ПАНДА-_-RYTP.mp4']
    ]

    searchHead = ['Category', 'ID', 'Channel/Category/Name', 'Video name']

    searchLayout = [
        # use screen keyboard
        [sg.Text('Video search')],
        [sg.Input(expand_x=True, key='-search-input'), sg.Button('Search', expand_x=True, key='-search')],
        # [sg.Radio(text='Film', group_id='filetype', key='-search-film'), sg.Radio(text='Document', group_id='filetype', key='-search-doc'), sg.Radio(text='Program', group_id='filetype', key='-search-program'), sg.Radio(text='Game', group_id='filetype', key='-search-game'), sg.Radio(text='All files', group_id='filetype', key='-search-alltypes', default=True)],
        # [sg.Radio(text='ID', group_id='filecategory', key='-search-byid', default=True), sg.Radio(text='Keywords in filename', group_id='filecategory', key='-search-bykeywords-filename'), sg.Radio(text='Keywords in Channel/Category/Name', group_id='filecategory', key='-search-bykeywords-channel')],
        [sg.Radio(text='ID', group_id='filecategory', key='-search-byid'), sg.Radio(text='Keywords and ID', group_id='filecategory', key='-search-all', default=True)],
        [sg.Table(values=searchTable, headings=searchHead, expand_y=True, expand_x=True, auto_size_columns=True, hide_vertical_scroll=False, display_row_numbers=False, key='-search-results')],

    ]


    torrTable = [
        ['Zootopia.mp4', 'Download', '8 MB/s', '2m 42s', '1,4GB'],
    ]
    torrHead = ['Torrent filename', 'Status', 'Speed', 'Time', 'Size of file']
    torrentLayout = [
        [sg.Text('Torrent manager')],
        [sg.Table(values=torrTable, headings=torrHead, expand_x=True, expand_y=True, auto_size_columns=True, hide_vertical_scroll=False, display_row_numbers=True)],
        [sg.Text('Torrent controls. '), sg.Input(tooltip='Number of row; Input via Video window', size=3, key='-torrent-row-number', justification='c'), sg.Button('Resume/Pause', key='-torrent-resume-pause'), sg.Button('Delete', key='-torrent-delete'), sg.Button('Get local link to file', key='-torrent-get-local-link'), sg.Button('Start/Stop torrent service', expand_x=True, key='-torrent-service-control'), sg.Button('Refresh list', key='-torrent-refresh', expand_x=True)],
    ]

    videoPlayer = [
        [sg.Image('', size=(806, 435), key='-VID_OUT-')],
    ]

    videoNumsTwo = [
        [sg.Text('List rebuild')],
        [sg.Button('YT', key='-rebuild-youtube-module'), sg.Button('Film', key='-rebuild-films-module'), sg.Button('Serial', key='-rebuild-serial-module')],
        # [sg.Button('Keywords maker', key='-keywords-maker', expand_x=True)],
        [sg.Text('Input box')],
        [sg.Button('Y', key='-video-y', size=(3, 1)), sg.Button('F', key='-video-film', size=(3, 1)), sg.Button('S', key='-video-serial', size=(3, 1))],
        [sg.Button('1', key='-video-1', size=(3, 1)), sg.Button('2', key='-video-2', size=(3, 1)), sg.Button('3', key='-video-3', size=(3, 1))],
        [sg.Button('4', key='-video-4', size=(3, 1)), sg.Button('5', key='-video-5', size=(3, 1)), sg.Button('6', key='-video-6', size=(3, 1))],
        [sg.Button('7', key='-video-7', size=(3, 1)), sg.Button('8', key='-video-8', size=(3, 1)), sg.Button('9', key='-video-9', size=(3, 1))],
        [sg.Button('<', key='-video-delchar', size=(3, 1)), sg.Button('0', key='-video-0', size=(3, 1)), sg.Button('C', key='-video-clearid', size=(3, 1))],
        [sg.Radio(text='Videos tab', group_id='toinput', key='-toinput-vids', default=True)],
        [sg.Radio(text='Torrent tab', group_id='toinput', key='-toinput-torrent')]
    ]

    videoLayout = [
        [sg.Column(videoPlayer, justification='c'), sg.Column(videoNumsTwo)],
        [sg.Input(key='-video-id-link', expand_x=True, default_text='URL or Video ID'), sg.Button('Load', key='-video-load'), sg.Button('Play', key='-video-play'), sg.Button('Pause', key='-video-pause'), sg.Button('Previous', key='-video-previous'), sg.Button('Next', key='-video-next'), sg.Button('Stop', key='-video-stop'), sg.Button('Clear', key='-video-clear'), sg.Text('Load', key='-video-msg-area')]
    ]

    musicLayout = [
        [sg.Text('Music player')]
    ]

    lifeLayout = [
        [sg.Text('Life control')]
    ]

    subsLayout = [
        [sg.Text('Subscriptions')]
    ]

    layout = [
        [sg.TabGroup(
            [[sg.Tab('Home', mainLayout, image_source=iconHome), 
            sg.Tab('Stats', systemStatsLayout, image_source=iconCPU), 
            sg.Tab('Settings', settingsLayout, image_source=iconSettings), 
            # sg.Tab('Torrents', torrentLayout, image_source=iconTorrent), 
            sg.Tab('Search', searchLayout, image_source=iconSearch),
            # sg.Tab('Music', musicLayout, image_source=iconMusic),
            sg.Tab('Video', videoLayout, image_source=iconVideo),
            # sg.Tab('Life', lifeLayout, image_source=iconLife),
            # sg.Tab('Subscriptions', subsLayout, image_source=iconSubs),
            ]], expand_y=True, expand_x=True, background_color='#0a0f14', key='-tab-name'
        )],
        [sg.Image(data=iconExit, key='-exit-app-main', enable_events=True, background_color='#0a0f14', tooltip='Exit from app'), sg.Text('', expand_x=True, background_color='#0a0f14'), sg.Image(data=iconLock, key='-lockscreen', enable_events=True, background_color='#0a0f14', tooltip='Lock screen'), sg.Text('23:29 31.12.1234', key='-main-time', background_color='#0a0f14')] # debug option
    ]

    lockLayout = [
        [sg.Text('Current time', key='-lock-time', background_color='Black', p=(0, (230, 10)))],
        [sg.Image(data=iconUnlock, key='-unlock', enable_events=True, background_color='Black')],
    ]
    sizeScreen = (1024, 600)
    # sizeScreen = (1920, 1080)
    window = sg.Window('Home center', layout, no_titlebar=True, size=sizeScreen, keep_on_top=True, font='Arial', background_color='#0a0f14').Finalize()
    windowLock = sg.Window('Lockscreen', lockLayout, no_titlebar=True, size=sizeScreen, keep_on_top=True, font='Arial', background_color='Black', element_justification='c').Finalize()
    windowLock.hide()
    lockEvent = None
    logging.info('Layouts created.')

    inst = vlc.Instance()
    list_player = inst.media_list_player_new()
    media_list = inst.media_list_new([])
    list_player.set_media_list(media_list)
    player = list_player.get_media_player()
    if PLATFORM.startswith('linux'):
        player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
    else:
        player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())
    logging.info('Player created')
    while True:
        event, values = window.read(timeout=10)
        if event!='__TIMEOUT__':
            print(event, values)
        if event == sg.WIN_CLOSED:           # always,  always give a way out!
            break
        if event == '-exit-app-main':
            break
        if event == '-exit-app-settings':
            break
        if event == '-lockscreen':
            windowLock.un_hide()
        lockEvent, lockValues = windowLock.read(timeout=10)
        now = datetime.datetime.now()
        created = now.strftime(r'%d/%m/%Y %H:%M:%S')
        createdn = now.strftime('%H:%M %d.%m.%Y')
        windowLock['-lock-time'].update(created)
        window['-main-time'].update(createdn)
        if lockEvent == '-unlock':
            windowLock.hide()
        if event == '-stats-reload':
            # сделано так, чтобы не перенагружать программу вечными прогрузками
            stats_cpu_load=str(psutil.cpu_percent(interval=1))
            stats_cpu_temp='0°'
            mem=psutil.virtual_memory()
            delitel = 1024 * 1024
            stats_mem_free=str(round(mem.free/delitel, 2))
            # stats_mem_full=str(round(mem.used/delitel, 2)+round(mem.free/delitel, 2))
            stats_mem_full=str(round((mem.used/delitel)+(mem.free/delitel), 2))
            stats_mem_usage=str(mem.percent)
            window['-stats_cpu_load'].update(value=str(stats_cpu_load+'%'))
            window['-stats_cpu_temp'].update(value=str(stats_cpu_temp))
            window['-stats_mem_free'].update(value=str(stats_mem_free+' MB'))
            window['-stats_mem_full'].update(value=str(stats_mem_full+' MB'))
            window['-stats_mem_usage'].update(value=str(stats_mem_usage+'%'))
        if lockEvent == '-unlock':
            windowLock.hide()
        if event == '-video-play':
            list_player.play()
        if event == '-video-pause':
            list_player.pause()
        if event == '-video-stop':
            list_player.stop()
        if event == '-video-next':
            list_player.next()
            list_player.play()
        if event == '-video-previous':
            list_player.previous()      # first call causes current video to start over
            list_player.previous()      # second call moves back 1 video from current
            list_player.play()
        if event == '-video-load':
            if values['-video-id-link'] and not 'URL or Video ID' in values['-video-id-link']:
                if os.path.exists(values['-video-id-link'])==True:
                    media_list.add_media(values['-video-id-link'])
                    list_player.set_media_list(media_list)
                    window['-video-id-link'].update('URL or Video ID')
                # else: pymsg.alert(title='Warning!', text='File not found')
                else: 
                    if fman.isVideoIDExist(values['-video-id-link']):
                        media_list.add_media(fman.getLinkId(values['-video-id-link']))
                    else:
                        pymsg.alert(title='Warning!', text='File not found')
        if event == '-video-clear':
            list_player = inst.media_list_player_new()
            media_list = inst.media_list_new([])
            list_player.set_media_list(media_list)
            player = list_player.get_media_player()
            if PLATFORM.startswith('linux'):
                player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
            else:
                player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())
            # pass
        if player.is_playing():
            window['-video-msg-area'].update("{:02d}:{:02d} / {:02d}:{:02d}".format(*divmod(player.get_time()//1000, 60),
                                                                        *divmod(player.get_length()//1000, 60)))
        else:
            window['-video-msg-area'].update('Load' if media_list.count() == 0 else 'Ready' )
        try:
            if event.split('-')[1] == 'video':
                if values['-toinput-vids']==True:
                    if event == '-video-y': window['-video-id-link'].update(values['-video-id-link']+str('y'))
                    elif event == '-video-serial': window['-video-id-link'].update(values['-video-id-link']+str('s'))
                    elif event == '-video-film': window['-video-id-link'].update(values['-video-id-link']+str('f'))
                    elif event.split('-')[2].isnumeric()==True: window['-video-id-link'].update(values['-video-id-link']+str(event.split('-')[2]))
                    else: pass
                else:
                    if event == '-video-y': window['-torrent-row-number'].update(values['-torrent-row-number']+str('y'))
                    elif event == '-video-serial': window['-torrent-row-number'].update(values['-torrent-row-number']+str('s'))
                    elif event == '-video-film': window['-torrent-row-number'].update(values['-torrent-row-number']+str('f'))
                    elif event.split('-')[2].isnumeric()==True: window['-torrent-row-number'].update(values['-torrent-row-number']+str(event.split('-')[2]))
                    else: pass
        except IndexError:
            pass
        except Exception as c:
            print(c)
            logging.fatal(traceback.format_exc())
        if event == '-video-clearid':
            if values['-toinput-vids']==True: window['-video-id-link'].update('')
            else: window['-torrent-row-number'].update('')
        if event == '-video-delchar':
            if values['-toinput-vids']==True: oldinf = values['-video-id-link']; window['-video-id-link'].update(oldinf[:-1])
            else: oldinf = values['-torrent-row-number']; window['-torrent-row-number'].update(oldinf[:-1])
        if event == '-rebuild-youtube-module': 
            fman.listRebuild(type='youtube')
        if event == '-rebuild-serial-module': 
            fman.listRebuild(type='serials')
        if event == '-rebuild-films-module': 
            fman.listRebuild(type='films')
        if event == '-search':
            """
            if values['-search-byid']==True:
                window['-search-results'].update(values=fileSearch.searchById(values['-search-input']))
            # if values['-search-bykeywords-channel']==True: #obsolete
            #     window['-search-results'].update(values=fileSearch.searchByChannel(values['-search-input'])) #obsolete
            """
            if values['-search-byid']==True:
                window['-search-results'].update(values=fileSearch.searchById(values['-search-input']))
            if values['-search-all']==True:
                window['-search-results'].update(values=fileSearch.search(values['-search-input']))
    window.close()
except Exception as c:
    print(c)
    logging.fatal(traceback.format_exc())
