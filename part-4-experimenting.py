import itertools
import logging

#full_ciphertext = "iettodcsoeinxeitmstokrcpirhuieynisgisnobsoixeohnuelraoonrrmeelecwt4lnetc dilufaeaiboerowh9ogrhtdsgmrtvvvzrnaodweawrmeiiaoeahaeeeierfebwzeaauorysnreuadycpnralejrtinnibttc llbokhthnab5cunisgloahdterusrhedcsbaleowoanniitdiraaevtkiesainiscedtrhocslsbahstcetsfttksteienkplerueheaiiiohosahcgatse3rillaprnonlcnhsetodhiebectodaepndlaeattosdendrmktcosfaseorsdhrftrbmaielhkwsusyeweaoeefoeoancmoecswlsodtfswyaanstidkbcbofofwutholsrstestnssrauiaroosherofeuesooeebatibldrroestnasrtifmqaenililitdl2ehgliehstlurgcodn shgv3nefldmehhiicienia qeoerereoealeenchnosnt6bboddxalnisolvekfwftgi38ndtstcltntcdaoloijhao2ndlhtieohceasufyrtaecnmdxueantweortal3mthkncge zcctsow niifteahleueoc2ak"
#full_ciphertext = "sstttehi"
full_ciphertext = "iettodcsoeinxeitmstokrcpirh"


# Set up a logger just in case the system crashes during runs
logging.basicConfig(filename="part-4-experimenting.log",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d|%(name)s|%(levelname)s|%(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.DEBUG)


with open("1-1000.txt", "r") as common_words_file:
    # Read the common words into a variable for speed
    common_words = [word for word in common_words_file.read().splitlines() if len(word) > 2]
    current = 0

    for permutation in itertools.permutations(full_ciphertext):
        _tmp = ''.join(permutation)
        _orig = _tmp

        matches = []
        for word in common_words:
            if word in _tmp:
                matches.append(word)
                _tmp = _tmp.replace(word, '')
        if len(matches) > 5:
            logging.warn("Hey, check this out!!!\n\n\n{}\n\nWords:{}".format(_orig, matches))

        current += 1
        if current % 5000 == 0:
            logging.info(f"Tried {current} iterations so far")

