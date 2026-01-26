import plotly.express as px
from pathlib import Path
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from bslib import bslib
from shiny import reactive
from shiny import ui, App, render, Inputs, Outputs, Session, req
from shinywidgets import render_plotly, output_widget
from dictionaries.hs_dicts import sect_dict as hs_dicts
import shinyswatch
import io
from shinyswatch import theme

data = pd.read_excel("C:/ERS/Statistics/Projects/Online Trade Data Platform/pract_env/prac3/data/Trade_2023_2025.xlsx"
                            , sheet_name='test2')

assets = Path(__file__).parent / "assets"

summary_page =     ui.page_fluid(


    ui.layout_column_wrap(

        ui.input_select("tradebal_filter",
                                     "Select Year",
                                     ['2023','2024', '2025' ],)

        ,
        ui.value_box(
                    "Total Trade",
                    ui.output_text("total_trade_value")
                ),


                ui.value_box(
                 "Import Value",
                    ui.output_text("total_import")
                ),
                ui.value_box(

                    "Export Value",
                    ui.output_text("total_export")
                ),

                fill= False,
    ),
    ui.br(),
    ui.br(),
    ui.layout_columns (
        ui.navset_card_tab (
            ui.nav_panel ("Monthly Trade", ui.layout_sidebar (
                ui.sidebar (
                    "Filter Options",

                    ui.input_selectize(
        "monthly_partner",
        "Select a Country",
        ['Republic of South Africa', 'Mozambique', 'India', 'Zimbabwe',
          'Botswana', 'United Kingdom','United Arab Emirates'],
        multiple=True,
        selected='Total'

    ),

                    ui.input_select("flow_filter",
                                     "Select Trade Flow",
                                     ["Total","Imports", "Exports"],)

                    ,


                ),
                         output_widget("monthly_trade")


            )        ),
         )
            ,

        ui.navset_card_tab (
            ui.nav_panel ("Top Trade Partners",
            output_widget("plot1"),
            ui.layout_columns (
                 ui.input_numeric("n_partner", "Top # Trade Partners", 5, min=0, max=10),
            )
        ),
        ui.nav_panel ("Top Commodities",
            output_widget("plot2"),
            ui.layout_columns (
                 ui.input_numeric("n_commodity", "Top # Commodities", 5, min=0, max=10),
            )
        )
    )

        ))

info_page = ui.page_fluid(

    ui.layout_columns(
        ui.card(

                ui.card_header (
                              ui.span("About Us", style="color: #2f2f31; font-weight: bold")
                          )

            ,
            ui.p("The Eswatini Revenue Service (ERS) is a semi-autonomous revenue administration agency. " \
            "It was set up through the Revenue Authority Act, 2008 (as amended). " \
            "The ERS works within the broad framework of Government but outside of the civil service." \
            "The ERS is structured" \
            " as a corporate entity and strives for operational excellence and efficiency."),

    ),
        ui.card(
            ui.card_header(
                ui.span("Harmonized System (HS) Codes", style="color: #2f2f31; font-weight: bold")
            ),
            ui.p("Among classification systems, Harmonized System (HS) codes " \
            "are commonly used throughout the import and export process for the" \
            " classification of goods. The Harmonized System is a standardized" \
            " numerical method of classifying traded products. It is used by countries" \
            " around the world to uniformly identify and describe products for purposes" \
            " such as assessing duties and gathering statistics."),

        ),


    ),

    ui.layout_columns(
        ui.card(

                ui.card_header (
                              ui.span("Basic Economic Categories Rev5 (BEC)", style="color: #2f2f31; font-weight: bold")
                          )
            ,
           ui.p("The Classification by Broad Economic Categories (BEC) Revision 5 organizes goods into categories " \
           "based on their main end-use (capital, intermediate, or consumption)"),

        ),
        ui.card(

                ui.card_header (
                              ui.span("Standard International Trade Classification Rev4 (SITC)", style="color: #2f2f31; font-weight: bold")
                          )
            ,
           ui.p("The Standard International Trade Classification (SITC) organizes traded products into sections, divisions, groups, and " \
           "subgroups based on materials, manufacturing stage, and industrial use. "),
        )
    ),
    )



app_ui = ui.page_fluid (

    # ui.input_checkbox("show", value=True),



    ui.include_css(Path(__file__).parent / "css/my-style.css"),

    ui.page_navbar(





    ui.nav_spacer(),

    ui.nav_panel (

        ui.span("Trade Summary",
                style="color: white; padding-right: 10px; font-weight: bold"), summary_page),



       ui.nav_panel ( ui.span("Trade Data",
                               style="color: white; font-weight: bold"),
          
        
                      
                      ui.br(),

                      ui.card (
                          ui.card_header (
                              ui.span("Refine Your Data Request", style="color: #2f2f31; font-weight: bold")
                          ),
                      ui.row (
                        
            ui.input_select("year_selection",
                             "Select Year",
                             ['2023','2024', '2025'],)
        ,

            ui.input_select("trade_flow_selection",
                             "Select Trade Flow",
                             ['Total', 'Imports', 'Exports']),

             ui.input_select("partner_selection",
                             "Search Trade Partner",
                             ['ZA : Republic of South Africa', 'BE : Belgium', 'IT : Italy', 'ZW : Zimbabwe',
          'BW : Botswana', 'GB : United Kingdom','KE : Kenya'],)
                             
                      ),


ui.row (
                        
            ui.input_select("mode_selection",
                             "Mode of Transport",
                             ['Road', 'Rail', 'Air', 'Sea', 'Multimodal', 'Unknown'],)
        ,

            ui.input_select("period_selection",
                             "Period (Year, Month)",
                             ['Total','January', 'February', 'March'],),

            ui.input_selectize("goods_search", "Search for Commodity",
                               multiple=True,
                               selected="Textile",
                               choices={"Textile" : "Textile", "Prepared Foodstuffs" : "Prepared Foodstuffs", 
                                        "Mineral Products" : "Mineral Products", "Machinery and Mechanical Appliances" : "Machinery and Mechanical Appliances",
                                        "Base Metals" : "Base Metals", "Vehicles" : "Vehicles", "Plastics" : "Plastics",
                                        "Vegatable Products" : "Vegatable Products", "Live Animals & Products" : "Live Animals & Products",
                                        
                                        })

                      )    
                      )
                      ,
                    

                      ui.download_button(
                         
                id="download_excel",
                label="Download Data",
                class_="btn-success",
                style="margin-top: 20px;",
            ),

            ui.input_action_button(
                id="btn2",
                label="Undo",
                class_="btn-success",
                style="margin-top: 20px;",
            ),

            ui.input_action_button(
                id="btn3",
                label="Redo",
                class_="btn-success",
                style="margin-top: 20px;",
            ),

            ui.br(),
            ui.br(),
            
                        
                        
                            
                        
                        
          ui.card (
              ui.card_header (ui.span("Trade Data Table", style="color: #2f2f31; font-weight: bold")   ),
            ui.output_data_frame("trade_df")  
          )                
                                            
            
                
            ),
            ui.nav_panel ( ui.span("Info Page",
                               style="color: white; font-weight: bold"), info_page),
          id="tabs",
          title= ui.span(
            ui.img(src = "ers logo.png", width= "40px", height= "40px"),
              
              ui.span("Eswatini Merchandise Trade", style= "color: #ffcc00; padding-left: 10px"),
            ui.span(" Data Request Platform", style = "color: white")
          ),
          # The footer argument accepts any UI elements
    footer=ui.div(
        ui.hr(),  # A horizontal line to separate content from footer
        ui.p("© 2026 Eswatini Revenue Service | Statistics Department", 
             style="text-align: center; background: #323491; color: white; padding: 20px;"),
        
    )   

          )

)


def server(input, output, session):
    @reactive.calc
    def total_trade():
        agg_trade = data.groupby(['Year']).agg({'SZLValue': 'sum'}).reset_index()


        filtered_agg = agg_trade[agg_trade['Year'] == int(input.tradebal_filter())]

        # if input.tradebal_filter() == 'All':




        total = filtered_agg['SZLValue'].sum()
        return total


    @reactive.calc
    def import_value():

        import_data = data[data['Flow'] == 'Imports']
        year_imports = import_data[import_data['Year'] == int(input.tradebal_filter())]
        agg_imports = year_imports.groupby(['Period', 'Partner',  'HS']).agg({'SZLValue': 'sum'}).reset_index()

        total_import = agg_imports['SZLValue'].sum()
        return total_import

    @reactive.calc
    def export_value():
        export_data = data[data['Flow'] == 'Exports']
        year_exports = export_data[export_data['Year'] == int(input.tradebal_filter())]
        agg_exports = year_exports.groupby(['Period', 'Partner',  'HS']).agg({'SZLValue': 'sum'}).reset_index()
        total_export = agg_exports['SZLValue'].sum()
        return total_export

    @reactive.calc
    def trade_filtered1():
        agg_trade = data.groupby(['Period', 'Partner', 'HS']).agg({'SZLValue': 'sum'}).reset_index()
        agg_filtered = agg_trade[agg_trade['Partner'].isin(input.partner_filter())]
        total = agg_filtered['SZLValue'].sum()
        return total

    @render.text
    def total_trade_value():
        return f"E{total_trade():,.0f}"

    @render.text
    def total_import():
        return f"E{import_value():,.0f}"

    @render.text
    def total_export():
        return f"E{export_value():,.0f}"

    @render_plotly
    def monthly_trade():
        monthly_data = data.groupby(['Month','Flow', 'Partner']).agg({'SZLValue': 'sum'}).reset_index()

        filtered_monthly = monthly_data[monthly_data['Partner'].isin(input.monthly_partner())]

        if input.flow_filter() == "Total":
            df = filtered_monthly
        else:
            df = filtered_monthly[filtered_monthly['Flow'] == input.flow_filter()]
        month_orders = calendar.month_name[1:]
        return px.bar(df, x='Month', y='SZLValue', category_orders = {'Month' : month_orders}, color="Flow"
                      , barmode='group', color_discrete_map={"Imports": "#323491", "Exports": "#ffcc00"})

    @render_plotly
    def partner_trade():



        patner_data = data.groupby(['Month', 'Partner', 'Flow']).agg({'SZLValue': 'sum'}).reset_index()
        partner_filtered = patner_data[patner_data['Partner'].isin(input.partner_filter())]


        return px.bar(partner_filtered, x='Partner', y='SZLValue', color="Flow",
                      barmode='group', color_discrete_map={"Imports": "#323491", "Exports": "#ffcc00"})

    @render.image
    def image():
        img = {"src": assets / "ers logo.png", "width": "60px", "height": "60px"}
        return img if input.show() else None


    @render_plotly
    def plot1():
        df = data


        partner = df.groupby('Partner')['SZLValue'].sum().nlargest(input.n_partner()).reset_index()

        return px.bar(partner, x='Partner', y="SZLValue")

    @render_plotly
    def plot2():
        df = data
        partner = df.groupby('Lib_Section')['SZLValue'].sum().nlargest(input.n_commodity()).reset_index()

        fig = px.bar(partner, x='Lib_Section', y="SZLValue")
        fig.update_xaxes(tickangle=-45)

        return fig

    @reactive.calc
    def commodity_filter():
        commodity = req(input.goods_search())
        commodity_data = data[data['Lib_Section'].isin(commodity)]
        return commodity_data


    @render.data_frame
    def trade_df():

            commodity_df = commodity_filter()


            year_df = commodity_df[commodity_df['Year'] == int(input.year_selection())]

            if input.trade_flow_selection() == "Total":
                flow_df = year_df
            else:
                flow_df = year_df[year_df['Flow'] == input.trade_flow_selection()]

            if input.period_selection() == "Total":
                period_df = flow_df
            else:
                period_df = flow_df[flow_df['Month'] == input.period_selection()]

            final_df = period_df
            return render.DataGrid(final_df,

                                )

    @render.download(
        filename="eswatini_trade_data.xlsx")
    async def download_excel():
        with io.BytesIO() as buf:
            commodity_df = commodity_filter()




            year_df = commodity_df[commodity_df['Year'] == int(input.year_selection())]

            year_df['APC'] = year_df['APC'].astype(str)
            year_df['HS'] = year_df['HS'].astype(str)

            if input.trade_flow_selection() == "Total":
                flow_df = year_df
            else:
                flow_df = year_df[year_df['Flow'] == input.trade_flow_selection()]

            if input.period_selection() == "Total":
                period_df = flow_df
            else:
                period_df = flow_df[flow_df['Month'] == input.period_selection()]

            final_df = period_df


            final_df.to_excel(buf, index=False, engine='openpyxl')
            yield buf.getvalue()





app = App(app_ui, server)






            # with ui.nav_panel("Table"):
            #     @render.table
            #     def table():
            #         return render.DataTable(data)

            # with ui.nav_panel("Visuals"):

            #     @render_plotly
            #     def plot1():
            #         df = data
            #         top_products = df.groupby('Partner')['SZLValue'].sum().nlargest(input.n()).reset_index()

            #         return px.bar(top_products, x='Partner', y="SZLValue")

