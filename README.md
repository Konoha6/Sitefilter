# Zbieranie stron przy użyciu Google API

cd Projects/sitefilter
./google.py szukana fraza
e /tmp/sitefilter/google-results  # w tym pliku pojawią się znalezione przez google strony, usuń niewłaściwe
./dulp.py
./rest2  # do tego pliku zostaną dopisane nowe strony


# Ręczne zbieranie stron

C+S+M+c - copyq kopiuje do 'clipboard/sitefilter'
C+S+M+v - copyq wkleja wszystko z 'clipboard/sitefilter' i czyści ten tab; wklej do:
/tmp/sitefilter/google-results  # usuń starą zawartość
./dupl.py
./rest2  # do tego pliku zostaną dopisane nowe strony
