# -*- coding: utf-8 -*-
from datetime import timedelta, date

from odoo import models, api,fields
class CrmLead(models.Model):
    """  Inherits crm.lead    """

    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self,interval):
       """ Fetches leads, opportunity , revenue , according to the interval given, current loggedin user and company and returns the result"""
       if interval == None:
           interval = 7
       interval = int(interval)
       date_time= fields.Date.today()-timedelta(days=interval)
       company_id = self.env.company
       leads = self.search([('company_id', '=', company_id.id),('user_id', '=', self.env.user.id),('create_date', '>=', date_time)])
       my_leads = leads.filtered(lambda r: r.type == 'lead')
       my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
       expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
       current_user=self.env.user.id
       my_revenue =sum( self.env['account.move'].search([('user_id', '=', current_user),('company_id', '=', company_id.id),('create_date', '>=', date_time)]).mapped('amount_total'))
       won_leads = leads.search_count([('stage_id.is_won', '=', True),('user_id', '=', self.env.user.id),('create_date', '>=', date_time)])
       lost_leads = leads.search_count([('active', '=', False), ('probability', '=', 0),('user_id', '=', self.env.user.id),('create_date', '>=', date_time)])
       # print('lost_leads',lost_leads)
       total = won_leads + lost_leads
       if total > 0:
           win_ratio = round(((won_leads / total) * 100),2)
       else:
           win_ratio = 0.0
       return {
           'total_leads': len(my_leads),
           'total_opportunity': len(my_opportunity),
           'expected_revenue': expected_revenue,
           'my_revenue': my_revenue,
           'my_win_ratio': win_ratio,
            'lost_leads': lost_leads,
       }

    @api.model
    def get_tiles_manager_data(self,interval):
        """fetch data to display for crm manager including every company datas """
        print('int',interval)
        if interval == None:
           interval = 7
        interval = int(interval)
        date_time = fields.Date.today() - timedelta(days=interval)

        leads = self.search(
           [ ('user_id', '=', self.env.user.id), ('create_date', '>=', date_time)])
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        current_user = self.env.user.id
        my_revenue = sum(self.env['account.move'].search(
           [('user_id', '=', current_user),
            ('create_date', '>=', date_time)]).mapped('amount_total'))
        won_leads = leads.search_count(
           [('stage_id.is_won', '=', True), ('user_id', '=', self.env.user.id), ('create_date', '>=', date_time)])
        lost_leads = leads.search_count(
           [('active', '=', False), ('probability', '=', 0), ('user_id', '=', self.env.user.id),
            ('create_date', '>=', date_time)])
        # print('lost_leads',lost_leads)
        total = won_leads + lost_leads
        if total > 0:
           win_ratio = round(((won_leads / total) * 100), 2)
        else:
           win_ratio = 0.0
        return {
           'total_leads': len(my_leads),
           'total_opportunity': len(my_opportunity),
           'expected_revenue': expected_revenue,
           'my_revenue': my_revenue,
           'my_win_ratio': win_ratio,
           'lost_leads': lost_leads,
        }

    @api.model
    def get_lost_leads(self,interval):
        """"Fetches lost leads according to the interval"""
        interval = int(interval)
        date_time= fields.Date.today()-timedelta(days=interval)
        company_id = self.env.company
        leads = self.search(
           [('company_id', '=', company_id.id), ('user_id', '=', self.env.user.id)])
        lost_leads = leads.search_count([('active', '=', False), ('probability', '=', 0),('user_id', '=', self.env.user.id),('create_date', '>=', date_time)])

        print('lost_leads',lost_leads)
        return {
           'lost_leads': lost_leads,
        }

    @api.model
    def date_calculation(self,interval):
        """Calculates date according to the interval"""
        interval=int(interval)
        date_time = fields.Date.today() - timedelta(days=interval)
        return date_time

    @api.model
    def leads_by_month(self):
        """Fetches month wise lead count """
        current_year = fields.Date.today().year
        company_id = self.env.company
        count=[]
        for mon in range(1,13):
           from_date=date(current_year,mon,1)
           next_month = from_date.replace(day=28) + timedelta(days=4)
           last_date = next_month - timedelta(days=next_month.day)
           print('from_date',from_date)
           print('last_date',last_date)
           leads = len(self.search([('company_id', '=', company_id.id), ('user_id', '=', self.env.user.id),('create_date','>=',from_date),('create_date','<=',last_date)]).ids)
           count.append(leads)
        return count