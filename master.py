import os
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from numerize.numerize import numerize as nm

company_data = pd.read_csv('./data/final.csv')
company_list = list(set(company_data['Code']))
company_list.sort()


selected_company_code = st.selectbox('Select Company:', (company_list))
asset = company_data[company_data['Code'] == selected_company_code]

latest = max(asset['Tahun - Kuartal'])
prev_period = str(int(latest[:4])-1) + ' - ' + latest[-1]

current_ratio_last = np.round(asset[asset['Tahun - Kuartal'] == latest]['Current Ratio'].values[0],2)
current_ratio_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Current Ratio'].values[0]
current_ratio_delta = np.round(current_ratio_last - current_ratio_prev, 2)

der_last = np.round(asset[asset['Tahun - Kuartal'] == latest]['Debt Equity Ratio'].values[0],2)
der_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Debt Equity Ratio'].values[0]
der_delta = np.round(der_last - der_prev, 2)

gpm_last = asset[asset['Tahun - Kuartal'] == latest]['Gross Profit Margin'].values[0]
gpm_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Gross Profit Margin'].values[0]
gpm_delta = gpm_last - gpm_prev

npm_last = asset[asset['Tahun - Kuartal'] == latest]['Net Profit Margin'].values[0]
npm_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Net Profit Margin'].values[0]
npm_delta = npm_last - npm_prev

roa_last = asset[asset['Tahun - Kuartal'] == latest]['Return on Asset'].values[0]
roa_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Return on Asset'].values[0]
roa_delta = roa_last - roa_prev

roe_last = asset[asset['Tahun - Kuartal'] == latest]['Return on Equity'].values[0]
roe_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Return on Equity'].values[0]
roe_delta = roe_last - roe_prev

rev_last = asset[asset['Tahun - Kuartal'] == latest]['Penjualan dan pendapatan usaha'].values[0]
rev_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Penjualan dan pendapatan usaha'].values[0]
rev_delta = (rev_last - rev_prev) / rev_prev

prf_last = asset[asset['Tahun - Kuartal'] == latest]['Jumlah laba (rugi)'].values[0]
prf_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Jumlah laba (rugi)'].values[0]
prf_delta = (prf_last - prf_prev) / prf_prev

eps_last = asset[asset['Tahun - Kuartal'] == latest]['Laba (rugi) per saham dasar dari operasi yang dilanjutkan'].values[0]
eps_prev = asset[asset['Tahun - Kuartal'] == prev_period]['Laba (rugi) per saham dasar dari operasi yang dilanjutkan'].values[0]
eps_delta = (eps_last - eps_prev) / eps_prev

current_ratio = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y='Current Ratio',
    tooltip=['Tahun - Kuartal', 'Current Ratio'])

debt_equity_ratio = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y='Debt Equity Ratio',
    tooltip=['Tahun - Kuartal', 'Debt Equity Ratio'])

gross_profit_margin = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y=alt.Y('Gross Profit Margin', axis=alt.Axis(format='%')),
    tooltip=['Tahun - Kuartal', 'Gross Profit Margin'])

net_profit_margin = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y=alt.Y('Net Profit Margin', axis=alt.Axis(format='%')),
    tooltip=['Tahun - Kuartal', 'Net Profit Margin'])

return_on_asset = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y=alt.Y('Return on Asset', axis=alt.Axis(format='%')),
    tooltip=['Tahun - Kuartal', 'Return on Asset'])

return_on_equity = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y=alt.Y('Return on Equity', axis=alt.Axis(format='%')),
    tooltip=['Tahun - Kuartal', 'Return on Equity'])

revenue = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y='Penjualan dan pendapatan usaha',
    tooltip=['Tahun - Kuartal', 'Penjualan dan pendapatan usaha'])

profit = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y='Jumlah laba (rugi)',
    tooltip=['Tahun - Kuartal', 'Jumlah laba (rugi)'])

eps = alt.Chart(asset).mark_bar().encode(
    x='Tahun - Kuartal',
    y='Laba (rugi) per saham dasar dari operasi yang dilanjutkan',
    tooltip=['Tahun - Kuartal', 'Laba (rugi) per saham dasar dari operasi yang dilanjutkan'])

st.markdown('**Latest Performance**')
st.markdown('Display current key metrics compared with same period in previous year')

col1, col2, col3 = st.columns(3)
col1.metric(label='Current Ratio', value=current_ratio_last, delta=current_ratio_delta)
col2.metric(label='Debt Equity Ratio', value=der_last, delta=der_delta, delta_color='inverse')
col3.metric(label='Gross Profit Margin (%)', value=np.round(gpm_last*100,2), delta=np.round(gpm_delta*100,2))

col4, col5, col6 = st.columns(3)
col4.metric(label='Net Profit Margin (%)', value=np.round(npm_last*100,2), delta=np.round(npm_delta*100,2))
col5.metric(label='Return on Asset (%)', value=np.round(roa_last*100,2), delta=np.round(roa_delta*100,2))
col6.metric(label='Return on Equity (%)', value=np.round(roe_last*100,2), delta=np.round(roe_delta*100,2))

col7, col8, col9 = st.columns(3)
col7.metric(label='Revenue (IDR), Growth (%)', value=nm(int(rev_last)), delta=np.round(rev_delta*100,2))
col8.metric(label='Profit (IDR), Growth (%)', value=nm(int(prf_last)), delta=np.round(prf_delta*100,2))
col9.metric(label='EPS (IDR), Growth (%)', value=eps_last, delta=np.round(eps_delta*100,2))

st.markdown('___')

st.altair_chart(current_ratio, use_container_width=True)
st.altair_chart(debt_equity_ratio, use_container_width=True)
st.altair_chart(gross_profit_margin, use_container_width=True)
st.altair_chart(net_profit_margin, use_container_width=True)
st.altair_chart(return_on_asset, use_container_width=True)
st.altair_chart(return_on_equity, use_container_width=True)
st.altair_chart(revenue, use_container_width=True)
st.altair_chart(profit, use_container_width=True)
st.altair_chart(eps, use_container_width=True)
