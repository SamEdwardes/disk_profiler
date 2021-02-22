import os
from collections import defaultdict

import pandas as pd
import plotly.express as px


def profile_disk(x):
    
    start_path = os.path.join(x)
    file_listing = defaultdict(list)

    for subdir, dirs, files in os.walk(start_path):
        for file_name in files:
            # extract meta data
            file_path = subdir + os.sep + file_name
            _, file_ext = os.path.splitext(file_name)
            byte_size = os.path.getsize(file_path)
            mb_size = byte_size / 1_000_000
            gb_size = mb_size / 1_000
            # add meta data to dict
            file_listing["file_name"].append(file_name)
            file_listing["file_ext"].append(file_ext)
            file_listing["parent"].append(subdir)
            file_listing["byte_size"].append(byte_size)
            file_listing["mb_size"].append(mb_size)
            file_listing["gb_size"].append(gb_size)
            file_listing["file_path"].append(file_path)
    
    return file_listing
        
data = profile_disk("C:\\Users\\sedwardes\\git")
data = pd.DataFrame(data)


def bar_chart(data, n=15, summary=False):
    if summary:
        data = data.groupby("parent")[["mb_size", "gb_size"]].agg("sum").reset_index(drop=False)
        y_axis = "parent"
    else:
        y_axis = "file_name"
    data = data.sort_values(by="mb_size", ascending=True)
    data = data.tail(n)
    fig = px.bar(
        data, 
        x="mb_size", 
        y=y_axis, 
        orientation="h",
        hover_data=["parent", "mb_size", "gb_size"],
        title=f"{n} Largest Files"
    )
    return fig

bar_chart(data, summary=True)