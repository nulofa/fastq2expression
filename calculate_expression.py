import os
import subprocess
import sys
import threading
import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import filedialog


window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('fastq to exp')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x400')  # 这里的乘是小x
# window.withdraw()
# 第4步，在图形界面上设定标签

ended = 'se'
def record_selection():
    global ended
    if var1.get() == 1:
        select_b1.config(stat='normal')
        select_b2.config(stat='disabled')
        ended = 'se'
        print(ended)
    elif var1.get() == 2:
        select_b1.config(stat='normal')
        select_b2.config(stat='normal')
        ended = 'pe'
        print(ended)



# 定义一个函数功能（内容自己自由编写），供点击Button按键时调用，调用命令参数command=函数名
on_hit2 = on_hit = False
file_path2 = old_path = file_path = ''
fn2 = fn = ''
def hit_me():
    global on_hit,file_path,old_path,fn
    if on_hit == False:
        t0.config(state='normal')
        on_hit = True
        old_path = file_path
        file_path = filedialog.askopenfilename()
        fn = file_path.split('/')[-1]
        t0.insert('end',file_path)
        t0.config(state='disabled')
    else:
        on_hit = False

def hit_me2():
    global on_hit2, file_path2, old_path, fn2
    if on_hit2 == False:
        t1.config(state='normal')
        on_hit2 = True
        file_path2 = filedialog.askopenfilename()
        fn2\
            = file_path2.split('/')[-1]
        t1.insert('end', file_path2)
        t1.config(state='disabled')
    else:
        on_hit2 = False

l = tk.Label(window, width=50, text='单端或双端 ?')
l.pack(pady=5)
var1 = tk.IntVar()  # 定义var1和var2整型变量用来存放选择行为返回值
var1.set(1)
r1 = tk.Radiobutton(window, text='单端',variable=var1, value=1, command=record_selection)
r1.pack(anchor="c")
r2 = tk.Radiobutton(window, text='双端',variable=var1, value=2, command=record_selection)
r2.pack(anchor="c")

# 第5步，在窗口界面设置放置Button按键
t0 = tk.Text(window, font=('Arial', 12), width=30, height=1)
t0.config(state='disabled')
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
t0.pack(pady=5)
select_b1 = tk.Button(window, text='选择fastq文件', font=('Arial', 12), width=10, height=1, command=hit_me)
select_b1.pack(pady=5)
t1 = tk.Text(window, font=('Arial', 12), width=30, height=1)
t1.config(state='disabled')
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
t1.pack(pady=5)
select_b2 = tk.Button(window, text='选择fastq文件', font=('Arial', 12), width=10, height=1, command=hit_me2)
select_b2.pack(pady=5)
select_b1.config(stat='normal')
select_b2.config(stat='disabled')


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()




def cal_exp(filename, out_path):
    gene_name = np.load('./gene_name2.npy')
    gn_dup = np.load('./gn_dup2.npy', allow_pickle=True).item()
    gn2ind = {}
    gene_len = len(gene_name)
    print(gene_len)
    for i in range(gene_len):
        gn2ind[gene_name[i]] = i
        if gene_name[i] in gn_dup:
            for gn in gn_dup[gene_name[i]]:
                gn2ind[gn] = i
    cnt_d = []
    with open(filename) as f:
        for line in f:
            if not line.startswith('gene-'):
                continue
            cont = line.split('\t')
            gn = cont[0].replace('gene-', '')
            if gn not in gn2ind:
                continue
            ind = gn2ind[gn]
            cnt = float(cont[-1])
            glen = float(cont[-2])
            cnt_d.append((gn, cnt , glen))
    count_data = pd.DataFrame(columns=['gene', 'count', 'length'], data= cnt_d)
    reads = count_data.loc[:, 'count']
    genes = count_data.loc[:, 'gene'].values
    glength = count_data.loc[:, 'length']
    rate = reads.values / glength.values
    tpm = rate / np.sum(rate, axis=0).reshape(1, -1) * 1e6
    with open(out_path, 'w') as f:
        f.write('gene\ttpm\n')
        for i in range(len(genes)):
            f.write(genes[i] + '\t' + str(tpm[0][i])+'\n')

def run_command(commd):
    return subprocess.check_output(commd, shell=True, stderr=subprocess.STDOUT)

def common_fn(fn1,fn2):
    a = len(fn1)
    b = len(fn2)
    minab = min(a, b)

    s = 'sample_'
    for i in range(minab):
        if fn1[i] == fn2[i]:
            s+= fn1[i]
        else:
            break
    return s

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def f2exp():
    from tkinter import scrolledtext
    t2 = scrolledtext.ScrolledText(window, font=('Arial', 12), height=10)
    t2.pack(pady=5)
    t2.config(state='disabled')
    r1.config(state='disabled')
    r2.config(state='disabled')
    select_b2.config(state='disabled')
    select_b1.config(state='disabled')
    run_b.config(state='disabled')

    global old_path, file_path,fn,ended,file_path2,fn2
    if old_path != file_path:
        old_path = file_path
        if ended == 'pe' and file_path2 != '':
            fn = fn.replace('.gz', '')
            fn2 = fn2.replace('.gz', '')
            if not os.path.exists('./tmp'):
                os.mkdir('tmp')

            t2.config(state='normal')
            t2.insert('end', 'QC ...\n')
            t2.config(state='disabled')
            i1 = file_path
            i2 = file_path2
            out1 = fn.replace('.fastq', '.p.fastq')
            out2 = fn.replace('.fastq', '.up.fastq')
            out3 = fn2.replace('.fastq', '.p.fastq')
            out4 = fn2.replace('.fastq', '.up.fastq')
            res = run_command('jre\\bin\\java -jar ./Trimmomatic-0.39/trimmomatic-0.39.jar PE -trimlog trim.log -threads 2 %s %s ./tmp/%s ./tmp/%s ./tmp/%s ./tmp/%s\
                        ILLUMINACLIP:./Trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:5:20 MINLEN:50'%(i1,i2,out1,out2,out3,out4))
            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\nhisat2-align ...\n')
            t2.config(state='disabled')
            comon_n = common_fn(fn, fn2)
            comon_n += '.fastq'

            sam_fn = comon_n.replace('.fastq', '.sam')
            res = run_command('cd hisat2.1 && hisat2-align-s.exe -p 2 --dta -x ./hisat_index/nnj -1 ../tmp/%s -2 ../tmp/%s -S ../tmp/%s' % (out1, out3, sam_fn))
            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\nsamtools ...\n')
            t2.config(state='disabled')
            bam_fn = sam_fn.replace('.sam', '.bam')
            res = run_command('cd SAMtools && samtools view -@ 2 -bS -o ../tmp/%s ../tmp/%s' % (bam_fn, sam_fn))
            sbam_fn = bam_fn.replace('.bam', '.s')
            res = run_command('cd SAMtools && samtools  sort -@ 2 ../tmp/%s ../tmp/%s' % (bam_fn, sbam_fn))
            sbam_fn += '.bam' #因为上一条命令会自动加.bam后缀
            res = run_command('cd SAMtools && samtools index ../tmp/%s' % sbam_fn)   #有问题

            subam_fn = sbam_fn.replace('s.bam', 'su.bam')
            res = run_command('cd SAMtools && samtools view -@ 2 -q 10 -F 1284 -f 0x02 -b ../tmp/%s > ../tmp/%s' % (sbam_fn, subam_fn))
            res = run_command('cd SAMtools && samtools index ../tmp/%s' % subam_fn)

            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\ncalculate expression ...\n')
            t2.config(state='disabled')

            cnt_fn = comon_n.replace('.fastq', '.count')
            res = run_command('cd featureCounts && featureCounts -p -a ../hisat2.1/hisat_index/nnj.gtf -g gene_id -o ../tmp/%s ../tmp/%s' % (cnt_fn, subam_fn))

            pref_n = len(fn)
            if '.gz' in file_path:
                pref_n += 3
            exp_outdir = file_path[:pref_n]+comon_n.replace('.fastq', '')+'_exp.txt'

            cal_exp('./tmp/'+cnt_fn, exp_outdir)
            #
            t2.config(state='normal')
            # #t2.insert('end', res.decode())
            t2.insert('end', '\n完成!\n样本表达谱(%s)已输出到与fastq文件同目录下' % comon_n.replace('.fastq', '.exp.txt'))
            t2.config(state='disabled')
            del_file('./tmp')

            select_b1.config(state='normal')
            select_b2.config(state='normal')
        elif ended == 'se':
            fn = fn.replace('.gz', '')
            t2.config(state='normal')
            t2.insert('end', 'QC ...\n')
            t2.config(state='disabled')
            if not os.path.exists('./tmp'):
                os.mkdir('tmp')
            res = subprocess.check_output( 'jre\\bin\\java -jar ./Trimmomatic-0.39/trimmomatic-0.39.jar SE -trimlog trim.log -threads 2 %s ./tmp/%s \
            ILLUMINACLIP:./Trimmomatic-0.39/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:5:20 MINLEN:50'%(file_path,fn.replace('.fastq','.clean.fastq'))
                                           , shell=True,stderr=subprocess.STDOUT)

            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\nhisat2-align ...\n')
            t2.config(state='disabled')
            res = subprocess.check_output('cd hisat2.1 && hisat2-align-s.exe --dta -x ./hisat_index/nnj -U ../tmp/%s -S ../tmp/%s' %
                                          (fn.replace('.fastq','.clean.fastq'), fn.replace('.fastq','.sam')),shell=True,stderr=subprocess.STDOUT)   #align

            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\nsamtools ...\n')
            t2.config(state='disabled')
            res = subprocess.check_output('cd SAMtools && samtools view -@ 2 -bS -o ../tmp/%s ../tmp/%s' % (fn.replace('.fastq','.bam'), fn.replace('.fastq','.sam')), shell=True,stderr=subprocess.STDOUT)
            res = subprocess.check_output('cd SAMtools && samtools sort -@ 2 ../tmp/%s ../tmp/%s' % (fn.replace('.fastq','.bam'), fn.replace('.fastq','.s')), shell=True,stderr=subprocess.STDOUT)  #SRR7536110.bam SRR7536110.s
            res = subprocess.check_output('cd SAMtools && samtools index ../tmp/%s' % fn.replace('.fastq','.s.bam'), shell=True,stderr=subprocess.STDOUT)
            res = subprocess.check_output('cd SAMtools && samtools view -@ 2 -q 10 -b ../tmp/%s > ../tmp/%s' % (fn.replace('.fastq','.s.bam'), fn.replace('.fastq','.su.bam')), shell=True,stderr=subprocess.STDOUT)
            res = subprocess.check_output('cd SAMtools && samtools index ../tmp/%s' % fn.replace('.fastq','.su.bam'), shell=True,stderr=subprocess.STDOUT)

            t2.config(state='normal')
            #t2.insert('end', res.decode())
            t2.insert('end', '\ncalculate expression ...\n')
            t2.config(state='disabled')

            res = subprocess.check_output('cd featureCounts && featureCounts -a ../hisat2.1/hisat_index/nnj.gtf -g gene_id -o ../tmp/%s ../tmp/%s'\
                                          % (fn.replace('.fastq','.count'),fn.replace('.fastq','.s.bam')), shell=True,stderr=subprocess.STDOUT)

            count_file = './tmp/' + fn.replace('.fastq', '.count')
            file_path = file_path.replace('.gz', '')
            cal_exp(count_file, file_path.replace('.fastq', '.txt'))

            t2.config(state='normal')
            # # #t2.insert('end', res.decode())
            t2.insert('end', '\n完成!\n样本表达谱(%s)已输出到与fastq文件同目录下' % (fn.replace('.fastq', '.txt')))
            t2.config(state='disabled')
            del_file('./tmp')
            select_b1.config(state='normal')
        else:
            select_b1.config(state='normal')
            t2.config(state='normal')
            t2.insert('end', '\n请选择fastq文件')
            t2.config(state='disabled')
    else:
        t2.config(state='normal')
        t2.insert('end', '\n请重新选择fastq文件')
        t2.config(state='disabled')
    select_b1.config(state='normal')
    select_b2.config(state='normal')
    run_b.config(state='normal')
    r1.config(state='normal')
    r2.config(state='normal')
    t0.config(state='normal')
    t1.config(state='normal')
    t0.delete('1.0', tk.END)
    t1.delete('1.0', tk.END)
    t0.config(state='disabled')
    t1.config(state='disabled')
run_b = tk.Button(window, text='run', font=('Arial', 12), width=10, height=1, command=lambda :thread_it(f2exp))
run_b.pack(pady=5)





# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。

