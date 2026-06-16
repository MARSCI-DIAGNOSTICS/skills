---
source_url: https://docs.cloud.google.com/monitoring/charts/metrics-explorer
source_type: llms-txt
content_hash: sha256:6a95fb0e27d2439b8b1d9a8be00fc79958c44a0a6a506a7adde556cde352e211
sitemap_url: https://geminicli.com/llms.txt
fetch_method: html
last_modified: '2026-03-16T16:17:42Z'
---

Create charts with Metrics Explorer  |  Cloud Monitoring  |  Google Cloud Documentation

[Skip to main content](#main-content)

[![Google Cloud Documentation](https://www.gstatic.com/devrel-devsite/prod/v8b8ef181e1dc913802015af34f7ea88ee446e0cb5daec5c977ac4c46a7a372bd/clouddocs/images/lockup.svg)](/)

`/`

[Console](//console.cloud.google.com/)

* English
* Deutsch
* Español
* Español – América Latina
* Français
* Indonesia
* Italiano
* Português
* Português – Brasil
* עברית
* 中文 – 简体
* 中文 – 繁體
* 日本語
* 한국어

Sign in

[![](https://docs.cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)](https://docs.cloud.google.com/monitoring/docs)

* [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs)

[Start free](//console.cloud.google.com/freetrial)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Observability](https://docs.cloud.google.com/docs/observability)
* [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs)
* [Guides](https://docs.cloud.google.com/monitoring/docs/monitoring-overview)

Send feedback

# Create charts with Metrics Explorer Stay organized with collections Save and categorize content based on your preferences.

This document describes how you can explore metric data by building a
temporary chart with Metrics Explorer. For example, to view the CPU
utilization of a virtual machine (VM), you can use Metrics Explorer to
construct a chart that displays the most recent data. If you want permanent
charts, then you can create a chart by using Metrics Explorer and
save it to a custom dashboard. An alternative is to create a custom dashboard,
which can display charts, logs, incidents, and other content, and then use
the dashboard interface to add charts to that dashboard.
For information about custom dashboards, see
[Create and manage custom dashboards](/monitoring/charts/dashboards).

You can create charts, such as those that chart a single metric type,
and complex charts, such as those that chart multiple metric types.
After you create a chart with Metrics Explorer, you can discard it,
save it to a custom dashboard, save its configuration, or share it.

The following screenshot shows a single
metric type—the CPU Utilization of a VM instance—charted on the
**Metrics Explorer** page:

![Metric charted using Metrics Explorer.](/static/monitoring/images/mip-me-instantiated.png)

The previous screenshot shows multiple lines, each line shows the average
CPU utilization for all VMs in a specific zone.

**Note:** If you are viewing a chart that is on a dashboard and want to view the
chart configuration or copy the chart to a different dashboard, then see if the
chart options let you view the chart Metrics Explorer. When you select
this option, Metrics Explorer is opened and displays the data you were
viewing. You can then view or modify the configuration,
or you can save the chart to a custom dashboard.

This feature is supported only for Google Cloud projects.
For [App Hub](/app-hub/docs/overview)
configurations, select the App Hub host project or management project.

## Chart a single metric type

To configure a chart to display a single metric, do the following:

1. In the Google Cloud console, go to the
   *leaderboard* **Metrics explorer** page:

   [Go to **Metrics explorer**](https://console.cloud.google.com/monitoring/metrics-explorer)

   If you use the search bar to find this page, then select the result whose subheading is
   **Monitoring**.
2. In the toolbar of the Google Cloud console,
   select your Google Cloud project. For [App Hub](/app-hub/docs/overview)
   configurations, select the App Hub host project or management project.
3. Specify the data to display on the chart. You can use a
   menu-driven interface, PromQL, or you can enter a
   Monitoring filter:

   ### Menu-driven interface

   1. Select the time series data that you want to view:

      1. In the **Metric** element, expand the **Select a metric** menu.

         The **Select a metric** menu contains features that help you find
         the metric types available:

         * To find a specific metric type, use the
           *filter\_list* **Filter bar**.
           For example, if you by enter `util`, then you restrict the menu to
           show entries that include `util`. Entries are shown when they pass
           a case-insensitive "contains" test.
         * To show all metric types, even those without data, click
           **done Active**. By default, the menus
           only show metric types with data.

      For example, you might make the following choices:

      1. In the **Active resources** menu, select **VM instance**.
      2. In the **Active metric categories** menu, select **uptime\_check**.
      3. In the **Active metrics** menu, select **Request latency**.
      4. Click **Apply**.
   2. Optional: To specify a subset of data to display,
      in the **Filter** element, select **Add filter**, and then
      complete the dialog. For example, you can view data for one zone by
      applying a filter. You can add multiple filters. For more information, see
      [Filter charted data](/monitoring/charts/metrics-selector#filter-option).

   For more information, see
   [Select the data to chart](/monitoring/charts/metrics-selector).
4. Combine and align time series:

   * To display every time series, in the **Aggregation** element,
     set the first menu to **Unaggregated** and the second menu to **None**.
   * To combine time series, in the **Aggregation** element,
     do the following:

     1. Expand the first menu and select a function.

        The chart is refreshed and displays a single time series. For example,
        if you select **Mean**, then the displayed time series is the average
        of all time series.
     2. To combine time series that have the same label values,
        expand the second menu, and then select one or more labels.

        The chart is refreshed and shows one time series for each unique
        combination of label values. For example, to display on time series
        per zone, set the second menu to **zone**.

        When the second menu is set to **None**, the chart displays one
        time series.
   * Optional: To configure the spacing between data points, click
     *add* **Add query element**, select **Min Interval**,
     and then enter a value.

   For more information about grouping and alignment, see
   [Choose how to display charted data](/monitoring/charts/metrics-selector#select_display).
5. Optional: To display only the time series with the highest or lowest
   values, use the **Sort & Limit** element.

### PromQL

1. In the toolbar of the
   query-builder pane, select the button whose name is either
   *code* **MQL** or *code* **PromQL**.
2. Verify that **PromQL** is selected
   in the **Language** toggle. The language toggle is in the same toolbar that
   lets you format your query.
3. Enter your query into the query editor. For example, to chart the average
   CPU utilization of the VM instances in your Google Cloud project, use the
   following query:

   ```
   avg(compute_googleapis_com:instance_cpu_utilization)
   ```

   For more information about using PromQL,
   see [PromQL in Cloud Monitoring](/monitoring/promql).

### Monitoring filter

1. In the **Metric** element, click *help\_outline* **Help**, and then
   select **Direct Filter Mode**.

   The **Metric** and **Filter** elements are deleted, and a **Filters** element
   that lets you enter text, is created.

   If you selected a resource type, metric,
   or filters before switching to **Direct Filter Mode** mode, then
   those settings are shown in the field of the **Filters** element.
2. Enter a Monitoring filter in the field of the
   **Filters** element.
3. Combine and align time series:

   * To display every time series, in the **Aggregation** element,
     set the first menu to **Unaggregated** and the second menu to **None**.
   * To combine time series, in the **Aggregation** element,
     do the following:

     1. Expand the first menu and select a function.

        The chart is refreshed and displays a single time series. For example,
        if you select **Mean**, then the displayed time series is the average
        of all time series.
     2. To combine time series that have the same label values,
        expand the second menu, and then select one or more labels.

        The chart is refreshed and shows one time series for each unique
        combination of label values. For example, to display on time series
        per zone, set the second menu to **zone**.

        When the second menu is set to **None**, the chart displays one
        time series.
   * Optional: To configure the spacing between data points, click
     *add* **Add query element**, select **Min Interval**,
     and then enter a value.

   For more information about grouping and alignment, see
   [Choose how to display charted data](/monitoring/charts/metrics-selector#select_display).

- Update the chart settings based on your selected metric type:

  * For quota metric types, use the following settings:

    + In the toolbar, set the time control to be at least one week. Quota
      metrics typically report one sample per day.
    + In the **Display** pane, expand the **Widget type**
      menu and then select **Stacked bar chart**.
  * For metric types that have a [`Distribution`](/monitoring/api/ref_v3/rest/v3/TypedValue#Distribution)
    value type, ensure that the **Widget type** menu is set to
    **Heatmap chart**. For more information, see
    [About distribution-valued metrics](/monitoring/charts/charting-distribution-metrics).
  * For other metric types, use the **Widget type** menu to display how the
    data is shown. The **Widget type** menu lists all available
    widget types; however, some widgets might not be enabled.
    Consider a chart that displays multiple time series, and assume that
    each measured value is a double:

    + **Line chart**, **Stacked bar chart**, and **Stacked area chart**
      widgets are listed as **Compatible**. You can select any of these types.
    + The **Heatmap** widget is disabled because these widgets can only display
      distribution-valued data.
- Optional: To change how a chart or table displays the selected data, use the
  options in the **Display** pane:

  * Chart options:

    + [**Analysis mode** menu](/monitoring/charts/chart-view-options#chart-modes):
      Select between line charts, x-ray, and statics.
    + [**Compare to Past** menu](/monitoring/charts/working-with-charts#comparetopast-option):
      Overlay current data with past data.
    + [**Threshold Line** menu](/monitoring/charts/working-with-legends#descr_template):
      add a reference threshold.
    + [**Legend Alias** menu](/monitoring/charts/working-with-legends#descr_template):
      configure the name of a legend column.
    + [**Y-axis assignment**, **Y-axis labels**, and **Y-axis scale** menus](/monitoring/charts/chart-view-options#logscale-option):
      Configure configure Y-axis assignment, labels, or scale.
  * Table options:

    + [**Value option** menu](/monitoring/charts#display-latest-or-aggregated):
      Select between the latest value and an aggregated value.
    + [**Visible columns** menu](/monitoring/charts#configure-visible-columns):
      Select which columns are shown.
    + [**Column formatting** menu](/monitoring/charts#configure-columns):
      Configure column names, alignment of data in a column, units,
      and whether cells are color-coded.
    + [**Metric view** menu](/monitoring/charts#reference-value):
      Select whether the value is show by itself or shown relative to a range of values.
    + [**Legend Alias** menu](/monitoring/charts/working-with-legends#descr_template):
      configure the name of a legend column.

## Chart multiple metric types

In some situations, you might want to display time series from different
metric types on the same chart. For example, to compare the read and write
loads on a VM, configure a chart to display the number of bytes
read and the number of bytes written.

To chart multiple metrics, you must use the menu-driven interface. The other
interfaces don't support charting multiple metrics.

To display multiple metrics on a chart, do the following:

1. In the Google Cloud console, go to the
   *leaderboard* **Metrics explorer** page:

   [Go to **Metrics explorer**](https://console.cloud.google.com/monitoring/metrics-explorer)

   If you use the search bar to find this page, then select the result whose subheading is
   **Monitoring**.
2. In the toolbar of the Google Cloud console,
   select your Google Cloud project. For [App Hub](/app-hub/docs/overview)
   configurations, select the App Hub host project or management project.
3. Specify the data to display on the chart.

   ### Menu-driven interface

   1. In the **Metric** element, and then select the
      first metric type whose data you want to view.
      For information about these steps, see
      [Chart a single metric type](#find-me).

      The query for this selection has the **A** identifier.
   2. For each additional metric type, do the following:

      1. Select **Add query**. A new query is added. For example, a query with the
         label **B** might be added.
      2. For the new query, in the **Metric** element, select a
         resource type and metric type. You can also add filters, combine time series,
         and sort and limit the number of displayed time series.

      The following screenshot illustrates the Metrics Explorer display
      when there are two metric types charted:

      ![Example of Metrics Explorer with two metric types.](/static/monitoring/images/eqb-two-metrics.png)
   3. Optional: In the **Display** pane,
      expand the **Y-axis** menu and configure which Y-axis is used for
      each metric type.

   ### PromQL

   Not supported.

   ### Monitoring filter

   Not supported.

## Chart a ratio of metrics

Monitoring the number of errors reported might be useful; however, it is
more likely that you need to monitor the rate of errors. That is, you
want to know how many errors occurred as measured against the total
number of responses. To meet this requirement, you can configure a chart
to display the ratio of two metrics. For references to examples and for
information about anomalies that can occur when you chart ratios of metrics,
see [Ratios of metrics](/monitoring/charts/metric-ratios).

To display a ratio of metrics on a chart, do the following:

1. In the Google Cloud console, go to the
   *leaderboard* **Metrics explorer** page:

   [Go to **Metrics explorer**](https://console.cloud.google.com/monitoring/metrics-explorer)

   If you use the search bar to find this page, then select the result whose subheading is
   **Monitoring**.
2. In the toolbar of the Google Cloud console,
   select your Google Cloud project. For [App Hub](/app-hub/docs/overview)
   configurations, select the App Hub host project or management project.
3. Specify the data to appear on the chart:

   ### Menu-driven interface

   1. Configure the numerator:

      1. In the **Metric** element, use the menus to select a
         resource type and metric type. For information about these steps, see
         [Chart a single metric type](#find-me).
      2. Update the aggregation fields. By default, averages all time series.
      3. Optional: Update the fixed length of time for points within a time series
         to be combined. To modify this field,
         click *add* **Add query element**,
         select **Min Interval**, and complete the dialog.
   2. Select **Add query** and then configure the denominator:

      1. For the new query, in **Metric** element, select a
         resource type and metric type.

         Select a metric type whose metric kind is the same as the numerator.
         For example, if the numerator metric is a `GAUGE` metric, then
         the select a `GAUGE` metric for the denominator.
      2. Update the aggregation fields.

         We recommend that the labels for the denominator metric type
         match the values set for the numerator metric type. For example,
         you might select the `zone` label for the numerator and denominator.

         You aren't required to use the same set of labels for both metric types;
         however, you can only select labels that are common to both
         metric types.
      3. Click *add* **Add query element**,
         select **Min Interval**, and ensure
         this field is set to the value that is used by the numerator.
   3. In the toolbar of the query pane, select **Create ratio**, and then
      complete the dialog.

      After you create the ratio, three queries are shown:

      * **A/B Ratio** identifies the ratio query.
      * **A** identifies the query for the numerator.
      * **B** identifies the query for the denominator.

      The following example illustrates a ratio that compares the sum of
      the bytes written to disk per zone, to the total number of bytes
      written to disk:

      ![Example of a ratio of metrics.](/static/monitoring/images/eqb-ratio-metrics.png)
   4. Optional: To switch the numerator and denominator metrics,
      in the **Ratio** element, expand the menu, and then make a selection.

   ### PromQL

   1. In the toolbar of the
      query-builder pane, select the button whose name is either
      *code* **MQL** or *code* **PromQL**.
   2. Verify that **PromQL** is selected
      in the **Language** toggle. The language toggle is in the same toolbar that
      lets you format your query.
   3. Enter your query into the query editor. For example, to chart the ratio of
      average latency of your `my_summary_latency_seconds` metric, use the
      following query:

      ```
      sum without (instance)(rate(my_summary_latency_seconds_sum[5m])) /
      sum without (instance)(rate(my_summary_latency_seconds_count[5m]))
      ```

      For more information about using PromQL,
      see [PromQL in Cloud Monitoring](/monitoring/promql).

   ### Monitoring filter

   Not supported.

## Save a chart for future reference

Metrics Explorer lets you create a chart that you can use to explore a
metric. However, the charts created by this tool aren't persistent. When you
navigate away from the Metrics Explorer page, the chart is discarded.

To save a chart you've configured with Metrics Explorer for future
reference, add the chart to a custom dashboard or save the chart's URL:

* To add the chart to a custom dashboard, do one of the following:

  + If you use the Google Cloud console to manage your custom dashboards,
    then select **Save Chart** in the Metrics Explorer toolbar,
    and complete the dialog. You can save the chart to an existing
    custom dashboard or you can create a dashboard.
  + If you use the Cloud Monitoring API to manage your custom dashboards,
    then update the JSON file that defines the dashboard and its
    contents. To access the JSON representation,
    click *code* **JSON Editor** in the chart toolbar.

    For detailed information
    about using the API to manage your custom dashboards, see
    [Create and manage dashboards by API](/monitoring/dashboards/api-dashboard).
* To keep a reference to the chart configuration, save the chart URL.
  Because the chart URL encodes the chart configuration, when you paste this
  URL into a browser the chart you configured is displayed.

  To obtain the chart's URL, click *link* **Link** in the chart
  toolbar.

## Save a chart's configuration

When you manage custom dashboards by using the Cloud Monitoring API, you
can use Metrics Explorer to help you construct the data you provide
to the API:

* To generate the JSON representation for a chart that you plan
  to add to a dashboard, configure the chart with Metrics Explorer.
  You can then use options within Metrics Explorer to view and copy
  the chart's JSON representation.
* To identify the syntax for a Monitoring filter,
  which is used with the Cloud Monitoring API, use the menu-driven interface
  of Metrics Explorer to configure the chart. After you select the
  metric and filters, switch to [direct filter mode](/monitoring/charts/metrics-selector#direct-filter)
  to view the equivalent Monitoring filter.

## Save the data displayed by the chart

To save the data displayed by the chart to your local system, click
*get\_app* **Download CSV**.

## What's next

* [Explore charted data](/monitoring/charts/working-with-charts)
* [Select metrics with Metrics Explorer](/monitoring/charts/metrics-selector)
* [View and manage metric usage](/monitoring/docs/metrics-management)
* [Set chart display options](/monitoring/charts/chart-view-options)

Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-16 UTC.

Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-03-16 UTC."],[],[]]
