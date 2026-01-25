import pandas as pd

hs_section = pd.read_excel("C:/ERS/Statistics/Projects/Online Trade Data Platform/Test Data/section_dict.xlsx", sheet_name="Sheet2")

code = hs_section['HS8']
name = hs_section['Short_Version']

sect_dict = dict(zip(code, name))