html_table_style = r'''
                    <style>
                    .table_component {
                        overflow: auto;
                        width: 100%;
                    }
                    
                    .table_component table {
                        border: 1px solid #dededf;
                        height: 100%;
                        width: 100%;
                        table-layout: fixed;
                        border-collapse: collapse;
                        border-spacing: 1px;
                        text-align: left;
                    }
                    
                    .table_component caption {
                        caption - side: top;
                        text-align: left;
                    }
                    
                    .table_component th {
                        border: 1px solid #dededf;
                        background-color: #eceff1;
                        color: #000000;
                        padding: 5px;
                    }
                    
                    .table_component td {
                        border: 1px solid #dededf;
                        background-color: #ffffff;
                        color: #000000;
                        padding: 5px;
                    }
                    </style>
'''

html_table_header = r'''
                    <div class="table_component" role="region" tabindex="0">
                    <table>
                        <caption>Table 1</caption>
                        <thead>
                            <tr>
                                <th>id</th>
                                <th>Fault Report Date</th>
                                <th>Equipment</th>
                                <th>Fault Category</th>
                                <th>Fault Description</th>
                                <th>EAMS WO #</th>
                                <th>Overdue (Days)</th>
                            </tr>
                        </thead>
                        <tbody>
'''

html_table_footer = r'''
                        </tbody>
                    </table>
                    </div>

'''
