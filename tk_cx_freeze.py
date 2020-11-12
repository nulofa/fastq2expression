import cx_Freeze
import sys


base = None
if sys.platform == 'win32':
    base = "Win32GUI"
include_file = ['hisat2.1',  'jre','gene_name2.npy', 'gn_dup2.npy','SAMtools', 'featureCounts','Trimmomatic-0.39']
executable  = [cx_Freeze.Executable('calculate_expression.py', base = base)]
# print(executable)
cx_Freeze.setup(
    name = 'fastq2exp',
    options = {'build_exe':{'packages': ['tkinter'], 'include_files':include_file}},
    version = '0.01',
    description = 'test fastq2exe',
    executables = executable
)

