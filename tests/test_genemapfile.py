import sys
import os
import unittest
from genemapfile.genemapfile import *
import re


class TestGeneMapFile( unittest.TestCase ):

    def setUp( self ):
        self.pm = GeneMapFile(file_to_parse='./tests/fixtures/hsa_gene_map.tab')
        self.pm.generate_map_data()

    def test_metabolic_map_number( self ):

        result =  self.pm.metabolic_line_data('POPTR_0001s00700g   00220 00330 01100 01110 04626')

        self.assertTrue( type( result['map_numbers'] ) is list )
        self.assertEqual( result['map_numbers'], [ '00220', '00330', '01100', '01110', '04626' ] )


    def test_metabolic_line_data( self ):

        result =  self.pm.metabolic_line_data('POPTR_0001s00700g   00220 00330 01100 01110 04626')

        self.assertTrue( type( result ) is dict )
        self.assertEqual( result['map_numbers'], [ '00220', '00330', '01100', '01110', '04626' ] )
        self.assertEqual( result['protein_identification'], 'poptr_0001s00700g' )


    def test_generate_map_data( self ):

        self.assertTrue( type( self.pm.protein_maps ) is dict )
        self.assertTrue( type( self.pm.organism_maps) is list )

    def test_maps_data( self ):

        self.assertTrue( type( self.pm.organism_maps) is list )

    def test_protein_identification_from_entry( self ):

        string = 'POPTR_0001s00700g   00220 00330 01100 01110 04626'

        expectedProteinId = 'poptr_0001s00700g' 

        proteinId = self.pm.protein_identification_from_entry( string )

        self.assertTrue( type( proteinId ) is str )
        self.assertEqual( proteinId, expectedProteinId )


    def test_protein_maps( self ):

        data = self.pm.protein_maps

        self.assertTrue( type( data ) is dict )
        self.assertTrue( len( data ) > 1 )


    def test_all_organism_maps( self ):

        data = self.pm.organism_maps

        self.assertTrue( type( data ) is list )
        self.assertTrue( len( data ) > 1 )


if __name__ == "__main__":
    unittest.main()
