:- use_module(library(musicbrainz)).
:- mb_search(artist,'Gorillaz',_Score,E), forall(mb_facet(E,F),(print(F),nl)).
:- halt.
