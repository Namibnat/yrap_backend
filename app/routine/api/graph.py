"""Build graphs for different routines"""

import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from routine.models import (StudyChunkScoreCardPages, StudyChunkScoreCard)

from django.conf import settings


class StudyChunkScoreCardGraph:
    def __init__(self, pk, reference, did_today=False):
        self.pk = pk
        self.item = reference
        self.did_today = did_today

    def make_graph(self):
        """Make graphs for study chunks
        
        Using Pandas and matplotlib, these graphs show a comparision
        between achieved scores and target scores.
        """
        today_text = "Today"
        if self.did_today:
            today_text += " (DONE!)"
        fileroute = f'routine/graphs/studychunk/{self.item}-graph.png'
        filename = os.path.join(settings.MEDIA_ROOT, fileroute)
        study_item = StudyChunkScoreCard.objects.get(pk=self.pk)
        study_days = StudyChunkScoreCardPages.objects.filter(reference=study_item)
        values = study_days.values()
        today = datetime.datetime.now().date()
        text_position = datetime.datetime.now() + datetime.timedelta(days=5)
        df = pd.DataFrame(values)
        df['date'] = df['date'].apply(lambda d: datetime.datetime.fromisoformat(str(d)).date())
        df = df.drop('id', axis=1)
        df = df.drop('reference_id', axis=1)
        df.set_index('date', drop=True, inplace=True)
        df = df.sort_index()
        average_page = df["target"].mean()
        std_offset = average_page + (df["target"].std()//3)
        fig, ax = plt.subplots(figsize=(15,9))
        _ = ax.set_title(f"Progress in {self.item}", color='#33ff33', fontsize=30, fontweight='bold')
        _ = ax.plot(df['achieved'], marker='o', markersize=1, color='b')
        _ = ax.plot(df['target'], marker='o', markersize=1, color='g')
        _ = ax.set_xlabel('Date', color='#33ff33', fontsize=20)
        _ = ax.set_ylabel('Pages', color='#33ff33', fontsize=20)
        _ = ax.axvline(datetime.datetime.now().date(), color='r')
        _ = ax.annotate(text=today_text,
                        xy=(today, average_page),
                        xytext=(text_position, std_offset),
                        arrowprops=dict(facecolor='#33ff33', shrink=0.05), color='#33ff33')
        _ = ax.spines[:].set_color('#535252')
        _ = ax.tick_params(axis='both', labelcolor='#33ff33')
        plt.savefig(filename, format='png', transparent=True)
        print(df)

        
        return f'/media/{fileroute}'
