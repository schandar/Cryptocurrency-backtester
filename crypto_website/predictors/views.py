import json
import traceback
import sys
import csv
import os

from operator import and_

from django.shortcuts import render
from django import forms

from backtester import backtester
from create_leaderboard import edit_board


class SearchForm(forms.Form):
    User_Name = forms.CharField(
        label='Username*:',
        required = True)
    start_date = forms.CharField(
        label="Start date*:",
        help_text='Format: yyyy-mm-dd. Date must be between 2016-01-01 and 2018-02-28.',
        required=True)
    end_date = forms.CharField(
        label='End date*:',
        help_text='Format: yyyy-mm-dd. Date must be between 2016-01-01 and 2018-02-28.',
        required=True)
    letter = forms.CharField(
        label='First character in ticker:',
        help_text ='e.g. A or 0',
        required=False)
    Twitter_Mentions = forms.IntegerField(
        label='Number of Twitter mentions on 2018-03-01 (lower bound):',
        help_text='Capped at 1000 mentions.',
        required=False)
    Google_Trends = forms.IntegerField(
        label='Growth in relative Google search frequency (lower bound):',
        help_text='e.g. Must be between 0 and 1000 (percent). If choosing this' + \
        ' option, must also select at least one of first ticker character,' + \
        ' complexity score, Twitter mentions, or total number of Reddit subscribers.',
        required=False)
    Reddit_Subscribers_Total = forms.IntegerField(
        label='Total number of reddit subscribers (lower bound):',
        help_text='e.g. Must be between 0 and 700000.',
        max_value=700000,
        min_value=0,
        required=False)
    Reddit_Subscribers_Growth = forms.IntegerField(
        label='Percent growth in number of reddit subscribers (lower bound):',
        help_text='e.g. Must be between 0 and 1000 (percent). If choosing this' + \
        ' option, must also select at least one of first ticker character,' + \
        ' complexity score, Twitter mentions, or total number of Reddit subscribers.',
        required=False)
    complexity_score = forms.IntegerField(
        label="Language complexity score for coin's white paper (lower bound):",
        help_text='e.g. Must be between 0 and 30.',
        max_value=30,
        min_value=0,
        required=False)
    

def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # Create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # Check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for backtester
            args = {}
            if form.cleaned_data["User_Name"]:
                args["User_Name"] = form.cleaned_data['User_Name']
            if form.cleaned_data['start_date']:
                args['start_date'] = form.cleaned_data['start_date']
            if form.cleaned_data['end_date']:
                args['end_date'] = form.cleaned_data['end_date']
            if form.cleaned_data['letter']:
                args['letter'] = form.cleaned_data['letter']
            if form.cleaned_data['Twitter_Mentions']:
                args['Twitter_Mentions'] = form.cleaned_data['Twitter_Mentions']
            if form.cleaned_data['Google_Trends']:
                args['Google_Trends'] = form.cleaned_data['Google_Trends']
            if form.cleaned_data['Reddit_Subscribers_Total']:
                args['Reddit_Subscribers_Total'] = form.cleaned_data['Reddit_Subscribers_Total']
            if form.cleaned_data['Reddit_Subscribers_Growth']:
                args['Reddit_Subscribers_Growth'] = form.cleaned_data['Reddit_Subscribers_Growth']
            if form.cleaned_data['complexity_score']:
                args['complexity_score'] = form.cleaned_data['complexity_score']
            
            try:
                # Check whether user's query returns any coins
                if len(backtester(args)) == 1:
                    res = backtester(args)
                else:
                    res = (backtester(args), edit_board(backtester(args)[1]))
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in backtester:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    
    
    if res is None:
        context['result'] = None
    elif len(res) == 1:
        context['result'] = res
    else:
        query, board = res
        columns = query[0]
        result = query[1]
        context['result'] = result
        context['columns'] = columns
        context['board'] = board

    context['form'] = form
    
    return render(request, 'index.html', context)

    
