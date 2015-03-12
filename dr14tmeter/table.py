# dr14_t.meter: compute the DR14 value of the given audiofiles
# Copyright (C) 2011  Simone Riva
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys


class Table:
    
    def __init__(self):
        self.__float_format = "%.2f"
        self.__col_cnt = 5
        self.__ini_txt = ""
        self.__txt = ""
    
    def _get_txt(self):
        return self.__txt
    
    def _set_txt( self , txt ):
        self.__txt = txt
        
    def _append_txt( self , txt ):
        self.__txt += txt 
        
    def init_txt(self, txt = "" ):
        self.__ini_txt = txt
    
    def new_table( self , txt ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_table( self , txt ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )

    def write_table(self):
        return self.__ini_txt + self._get_txt()
        
    def nl(self):
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return '\n'
        elif sys.platform.startswith('win'):
            return '\n\r'
    
    def format_element( self , el ):
        if isinstance( el , float ) :
            return "%s" % self.__float_format % el
        else :
            return str( el )
    
    def append_row( self , row_el , cell_type='d'):
        
        if cell_type == 'd':
            n_cell = self.new_cell
            e_cell = self.end_cell
        elif cell_type == 'h':
            n_cell = self.new_hcell
            e_cell = self.end_hcell
        
        self.new_row()
        
        for i in row_el:
            n_cell()
            self.add_value( i )
            e_cell()
            
        self.end_row()

    def get_col_cnt( self ):
        return self.__col_cnt
    
    def set_col_cnt( self , col_cnt ):
        self.__col_cnt = col_cnt
        
    col_cnt = property( get_col_cnt , set_col_cnt )
    
    def append_separator_line( self ):
        self._append_txt( self.format_element( "" ) )
    
    def append_closing_line( self ):
        self._append_txt( self.format_element( "" ) )
        
    def append_empty_line( self ):
        self.append_row( [ "" ]*self.col_cnt )

    def add_title( self , title ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
        
    def add_value( self , val ):
        self._append_txt( self.format_element(val) )
        
    def new_head( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_head( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_tbody( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_tbody( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_foot( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_foot( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_row( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_row( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def new_cell( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_cell( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def new_hcell( self ):
        return self.new_cell()
    
    def end_hcell( self):
        return self.end_cell()
    
    def new_bold( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_bold( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    
    

class TextTable ( Table ):

    def append_separator_line( self ):
        self.append_row( [ "----------------------------------------------------------------------------------------------" ] )

    def append_closing_line( self ):
        self.append_row( [ "==============================================================================================" ] )
    
    def append_empty_line( self ):
        self.append_row( [ "" ] ) 

    def add_title( self , title ):
        self._append_txt( title + self.nl() )

    def new_table( self ):
        self._set_txt("")
    
    def end_table( self ):
        self._append_txt( self.nl() )
    
    def new_row( self ):
        self._append_txt("")
    
    def end_row( self ):
        self._append_txt( self.nl() )
    
    def new_cell( self ):
        self._append_txt("")
    
    def end_cell( self ):
        self._append_txt( "\t" )
    
    def new_bold( self ):
        self._append_txt("")
    
    def end_bold( self ):
        self._append_txt("")
    
    

class BBcodeTable ( Table ):

    def append_separator_line( self ):
        self.append_row( [ "------------" ] * self.col_cnt )

    def append_closing_line( self ):
        self.append_row( [ "============" ] * self.col_cnt )

    def add_title( self , title ):
         self._append_txt( self.nl() + "[tr]" + self.nl() + " [td  colspan=%d] " % self.col_cnt + title + " [/td] " + self.nl() + "[/tr]" + self.nl() )

    def new_table( self ):
        self._set_txt("")
        self._append_txt( '[table]' + self.nl() )
    
    def end_table( self ):
        self._append_txt( self.nl() + '[/table]' + self.nl() ) 
    
    def new_row( self ):
        self._append_txt( self.nl() + '[tr]' + self.nl() )
    
    def end_row( self ):
        self._append_txt( self.nl() + '[/tr]' + self.nl() )
    
    def new_cell( self ):
        self._append_txt( ' [td]' )
    
    def end_cell( self ):
        self._append_txt( '[/td]' )
    
    def new_bold( self ):
        self._append_txt( '[b]' )
    
    def end_bold( self ):
        self._append_txt( '[/b]' )


class HtmlTable ( Table ):

    def add_title( self , title ):
        self._append_txt( self.nl() + "<tr>" + self.nl() + " <th colspan=\"%d\" > " % self.col_cnt + title + "</th>" + self.nl() + "</tr>" + self.nl() ) 

    def new_table( self ):
        self._set_txt("")
        self._append_txt( "<table>" + self.nl() ) 
    
    def end_table( self ):
        self._append_txt( self.nl() + "</table>" + self.nl() )
        
    def new_head( self ):
        self._append_txt( self.nl() + "<thead>" + self.nl() ) 
    
    def end_head( self ):
        self._append_txt( self.nl() + "</thead>" + self.nl() )
        
    def new_tbody( self ):
        self._append_txt( self.nl() + "<tbody>" + self.nl() ) 
    
    def end_tbody( self ):
        self._append_txt( self.nl() + "</tbody>" + self.nl() ) 
    
    def new_foot( self ):
        self._append_txt( self.nl() + "<tfoot>" + self.nl() ) 
    
    def end_foot( self ):
        self._append_txt( self.nl() + "</tfoot>" + self.nl() ) 
    
    def new_row( self ):
        self._append_txt( self.nl() + "<tr>" + self.nl() ) 
    
    def end_row( self ):
        self._append_txt( self.nl() + "</tr>" + self.nl() ) 
    
    def new_cell( self ):
        self._append_txt( ' <td>' )
    
    def end_cell( self ):
        self._append_txt( '</td>' )
    
    def new_hcell( self ):
        self._append_txt( ' <th>' )
    
    def end_hcell( self ):
        self._append_txt( '</th>' )
    
    def new_bold( self ):
        self._append_txt( '<b>' )
    
    def end_bold( self ):
        self._append_txt( '</b>' )


class MediaWikiTable ( Table ):

    def add_title( self , title ):
        self._append_txt( "|-" + self.nl() + "!align=\"left\" colspan=\"%d\" | " % self.col_cnt + title + self.nl() )

    def new_table( self ):
        self._set_txt("")
        self._append_txt( "{| " + self.nl() ) 
    
    def end_table( self ):
        self._append_txt( "|}" + self.nl() )
        
    def new_row( self ):
        self._append_txt( "|-" + self.nl() ) 
    
    def end_row( self ):
        self._append_txt( self.nl() )
    
    def new_cell( self ):
        self._append_txt( '||' )
    
    def end_cell( self ):
        self._append_txt( "" )
        
    def new_bold( self ):
        self._append_txt( "\'\'\'" )
    
    def end_bold( self ):
        self._append_txt( "\'\'\'" )
        
     
class row:
    def __init__(self):
        self.row = []
        self.inds = []
        self.type = "l"
    
    def set_type(self, t):
        self.type = t 
    
    @property
    def set_row(self):
        self.set_type("r")
        return self.type

    @property        
    def set_title(self):
        self.set_type("t")
        return self.type
        
    @property        
    def set_separator_line(self):
        self.set_type("sl")
        return self.type
    
    @property    
    def set_closing_line(self):
        self.set_type("cl")
        return self.type                        
    
    @property
    def is_row(self):
        if self.type == "r" :
            return True
        else :
            return False
    
    @property        
    def is_title(self):
        if self.type == "t" :
            return True
        else :
            return False
        
    @property        
    def is_separator_line(self):
        if self.type == "sl" :
            return True
        else :
            return False
    
    @property        
    def is_closing_line(self):
        if self.type == "cl" :
            return True
        else :
            return False
        
         
    
        
class ExtendedTextTable ( Table ):
    
    def __init__(self):
        super(ExtendedTextTable,self).__init__()
        self._cols_sz = [0] * super(ExtendedTextTable,self).get_col_cnt()
        self._rows = []
    
    def get_col_cnt( self ):
        return super(ExtendedTextTable,self).get_col_cnt()
    
    def set_col_cnt( self , col_cnt ):
        super(ExtendedTextTable,self).set_col_cnt( col_cnt )
        
        if len( self._cols_sz ) < col_cnt :
            self._cols_sz = self.col_sz[:col_cnt] 
        elif len( self._cols_sz ) > col_cnt :
            for n in range(len( self._cols_sz ), col_cnt):
                self._cols_sz.append(0)
                
    col_cnt = property( get_col_cnt , set_col_cnt )
       
    
    def new_table( self , txt ):
        self._cols_sz = [0] * self.col_cnt
        self._rows = []
    
    def end_table( self , txt ):
        pass    
    
    def append_separator_line( self ):
        r = row()
        r.set_separator_line
        self._rows.append( r )
    
    def append_closing_line( self ):
        r = row()
        r.set_closing_line
        self._rows.append( r )
        
    def append_empty_line( self ):
        self.append_row( [ "" ]*self.col_cnt )

    def add_title( self , title ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
        
    def add_value( self , val ):
        self._append_txt( self.format_element(val) )
        
    def new_head( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_head( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_tbody( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_tbody( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_foot( self ):
        self._append_txt( self.format_element( "" ) )
    
    def end_foot( self ):
        self._append_txt( self.format_element( "" ) )
    
    def new_row( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_row( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def new_cell( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_cell( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def new_hcell( self ):
        return self.new_cell()
    
    def end_hcell( self):
        return self.end_cell()
    
    def new_bold( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def end_bold( self ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )    
    

