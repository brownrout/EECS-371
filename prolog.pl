:- use_module(library(musicbrainz)).
:- mb_search(artist,'John Coltrane',Score,E), forall(mb_facet(E,F),(print(F),nl)).
:- halt.
