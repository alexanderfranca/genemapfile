# -*- coding: utf-8 -*-

import pprint

from genemapfile.genemapfile import *

gm = GeneMapFile('./tests/fixtures/hsa_gene_map.tab')

data = gm.generate_map_data() 

pprint.pprint(gm.protein_maps['5338'])
