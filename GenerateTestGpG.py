import sys
from GPG_Pos_Dist import*
from random import randint
from time import sleep

class pseudo_usd_sample:
    num_version = 1
    lim=250
    def generate_sample(self,sample, base_usd,num_usd):
        one_sample = GPG_Pos_Dist_Element()
        istepa = 45
        istepb = 5
        icurrenta = -90
        istepusd = 00
        while icurrenta<91:
            icurrentb = -15
            while icurrentb<16:
                usd = []
                for add_usd in range(num_usd):
                    usd.append(base_usd)

                one_sample.set_all(0,0,icurrenta,icurrentb)
                one_sample.set_all_usd(usd,num_usd)
                sample.add_element(one_sample)
                base_usd = base_usd+istepusd
                icurrentb = icurrentb+ istepb
            icurrenta = icurrenta + istepa

if __name__ == "__main__":
    if len(sys.argv) !=2:
        print 'usage: GenerateTestGpG.py <path_to_file_to_save> \n You must specify the path to the file you want to save as the first arg'
        sys.exit(1)
    filename = sys.argv[1]
    test_acquire = pseudo_usd_sample()
    test = GPG_Pos_Dist()
    test.release_element()

    test_acquire.generate_sample(test,100,5)

    io = GPG_Pos_Dist_IO(test.get_version())
    info = 'Generated by GenerateTestGpG.py version :'+str(test_acquire.num_version)
    io.ToFile(test,filename,info)

