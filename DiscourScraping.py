from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import os

class DiscScrap():
    
    def __init__(self, Dir):
        self.url = "http://www.maroc.ma/fr/discours-du-roi?field_type_discours_royal_value_i18n=1&date_discours%5Bvalue%5D%5Byear%5D="
        self.page = 0
        self.Dir = self.__make_Dir(Dir)

    def __get_bs_page(self, url):   
        Cl = uReq(url)
        page = Cl.read()
        Cl.close()
        return bs(page, "html.parser")

    def __make_Dir(self, Dir):
        try: os.mkdir(Dir)
        except: print('[WARNING]: Dir already exist, working with current Dir.....')
        return Dir

    def __get_disc(self, disc_p):
        Discour = ""
        for element in disc_p:
            Discour = Discour + element.text + "\n"
        return Discour  

    def __disc(self, discours, year ,page):
        discours_p = discours.ul.findAll("li")
        i = page*6
        for element in discours_p:
                    Ref = "http://www.maroc.ma"+element.span.h2.a["href"]
                    bs_FTP = self.__get_bs_page(Ref)
                    Discour_p = bs_FTP.findAll("p")
                    Discour = self.__get_disc(Discour_p)
                    path = os.path.join(self.Dir, str(year)+'_D_'+str(i))
                    i += 1
                    with open(path, 'w') as f:
                        f.write(Discour)

        return




    def main(self):
        for year in range(2019, 1998, -1):
            self.page = 0
            w_url = self.url+str(year) 
            while (True):
                bs0 = self.__get_bs_page(w_url)
                try :
                    discours = bs0.findAll("div",{"class":"discours"})[0]
                except IndexError:
                    break

                self.__disc(discours, year, self.page)
                self.page += 1 
                w_url = w_url+"&page="+str(self.page)


if __name__ == '__main__':
    inst = DiscScrap('Disc_Text')
    inst.main()
    print('[info]   ******* DONE SCRAPING ********')
                