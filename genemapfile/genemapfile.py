import re
import pprint
import glob
import sys
import os

class GeneMapFile:
    """
    Deals with pathway organism _gene_map.tab files.

    Those files have the relation between metabolic map numbers and genes/proteins identification.

    Attributes:
        organism_gene_map_file (file): File handle for the organism _gene_map.tab file.
        protein_maps (dict): Proteins/Genes and its maps.
        organism_maps (list): Orgaism and its metabolic maps.
        organism_code (str): KEGG 3 or 4 letter organism code.

    """
    def __init__(self, file_to_parse):

        self.file_to_parse = file_to_parse
        self.protein_maps  = {}
        self.organism_maps = [] 
        self.organism_code = None

    def protein_identification_from_entry( self, string=None ):
        """
        Returns the protein identification found in an entry.
        
        That kind of entry is something like: 'POPTR_0001s00700g   00220 00330 01100 01110 04626' 

        An entry line can have only a single protein identification (POPTR_0001s00700g for example).

        Args:
            string(str): An entry line.

        Returns:
            (list): The protein identification.
        """
        
        result = self.metabolic_line_data( string )
        result = result['protein_identification']

        return result


    def metabolic_line_data( self, string=None ):
        """
        Returns a entry line in a dictionary format, identifying protein identification and map numbers.

        That kind of string is something like: 'POPTR_0001s00700g   00220 00330 01100 01110 04626'

        Args:
            string(str): An entry line.

        Returns:
            (dict): Protein identification and map numbers 

        """

        string = re.sub( '\s', ':', string )
        string = re.sub( '\:{1,}', ':', string )
        re_map = re.split(':', string )

        protein_identification = re_map[0]
        protein_identification = protein_identification.lower() 

        map_numbers = re_map[1:] 

        result = { 'protein_identification': protein_identification, 'map_numbers': map_numbers }

        return result



    def metabolic_map_number( self, string=None ):
        """
        Returns the metabolic map numbers from a string.

        That kind of string is something like: 'POPTR_0001s00700g   00220 00330 01100 01110 04626'

        Args:
            string(str): File line/string to be parsed.

        Returns:
            (list): Map numbers
        """

        result = self.metabolic_line_data( string )
        result = result['map_numbers']

        return result


    def generate_map_data(self):
        """
        Read $organism_gene_map.tab and fills some important dictionaries: protein_maps and organism_maps.

        Returns:
            (void): Only create and fills class dictionaries. 
        """

        # ----------------------------------------------------------------------------------------------------------------------
        #
        # Not so important... but really important: protein/genes identification will be converted to lower case. Why?
        # We never know the case of the annotatoins.
        # 
        # ----------------------------------------------------------------------------------------------------------------------
        self.organism_maps = []
        self.protein_maps  = {}

        with open(self.file_to_parse) as f:
            for line in f:
                line = line.rstrip('\r\n')

                map_number = self.metabolic_map_number( line )
                protein_identification = self.protein_identification_from_entry( line )
                protein_identification = protein_identification.lower()

                if not protein_identification in self.protein_maps: 
                    self.protein_maps[ protein_identification ] = [] 

                self.organism_maps.extend( map_number )
                
                self.protein_maps[ protein_identification ].extend( map_number )
                self.protein_maps[ protein_identification ] = set( self.protein_maps[ protein_identification ] )
                self.protein_maps[ protein_identification ] = list( self.protein_maps[ protein_identification ] )

        self.organism_maps = set( self.organism_maps )
        self.organism_maps = list( self.organism_maps )

        return self.protein_maps

    def protein_maps( self ):
        """
        Returns a dictionary containing proteins and its metabolic pathway maps.

        Returns:
            (dict): Dictionary with all metabolic maps number.
        """

        return self.protein_maps


    def organism_maps( self ):
        """
        Returns a list containing metabolic pathway maps number.

        Returns:
            (dict): Llist with all metabolic maps number.
        """

        return self.organism_maps

