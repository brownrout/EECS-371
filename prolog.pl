:- use_module(library(musicbrainz)).
:- mb_search(artist,'Creed',_Score,E), forall(mb_facet(E,F),(print(F),nl)).
:- halt.
