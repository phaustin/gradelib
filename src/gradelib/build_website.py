



class_dir = Path('e211_labs')
class_dir.mkdir(exist_ok=True,parents=True)
for sname in sname_dict.keys():
    new_dir = class_dir / sname
    new_dir.mkdir(exist_ok=True, parents=True)
    sname_dict[sname]['dirpath']=new_dir
    canvas_id = sname_dict[sname]['canvas_id']
    name_dict[canvas_id]['dirpath']=new_dir.resolve()

def add_lab(name_dict,lab_dir,lab_name):
    """
    add an html path to a sname_dict entry
    """
    file_list = list(lab_dir.glob(f'**/{lab_name}'))
    for the_file in file_list:
        parts = the_file.parts
        if str(lab_dir).find('feedback') > -1:
            canvas_id = parts[-3]
            key = lab_name
        else:
            filename=the_file.parts[-1]
            parts=filename.split('_')
            canvas_id = parts[-4]
            # remove the *
            key = lab_name[1:]
        try:
            name_dict[canvas_id]['html_files'][key]=the_file
        except KeyError:
            pass


feedback_dir = Path.home() / 'repos/nbgrader_dir/feedback'
for the_lab in ['lab_wk2.html','lab_wk8.html','lab_wk9.html','lab_wk11.html']:
    add_lab(name_dict, feedback_dir, the_lab)
        
