TARGETS = \
	var/name.basics.tsv \
	var/title.akas.tsv \
	var/title.basics.tsv \
	var/title.crew.tsv \
	var/title.episode.tsv \
	var/title.principals.tsv \
	var/title.ratings.tsv \

all: ${TARGETS}

var:
	mkdir var

var/%.tsv.gz: var
	cd var ; wget https://datasets.imdbws.com/$*.tsv.gz

var/%.tsv: var/%.tsv.gz
	cd var ; gunzip $*.tsv.gz

