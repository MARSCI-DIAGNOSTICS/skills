---
source_url: https://docs.cloud.google.com/trace/docs/finding-traces
source_type: llms-txt
content_hash: sha256:8ecf114ee466a47e5de6548aecab2ee8db286add4d7368a793e418819e73e48f
sitemap_url: https://geminicli.com/llms.txt
fetch_method: html
last_modified: '2026-03-19T19:19:39Z'
---

Find and explore traces  |  Cloud Trace  |  Google Cloud Documentation

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
* 中文 – 简体
* 中文 – 繁體
* 日本語
* 한국어

Sign in

[![](https://docs.cloud.google.com/_static/clouddocs/images/icons/categories/observability-color.svg)](https://docs.cloud.google.com/trace/docs)

* [Cloud Trace](https://docs.cloud.google.com/trace/docs)

[Start free](//console.cloud.google.com/freetrial)

* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Observability](https://docs.cloud.google.com/docs/observability)
* [Cloud Trace](https://docs.cloud.google.com/trace/docs)
* [Guides](https://docs.cloud.google.com/trace/docs/overview)

Send feedback

# Find and explore traces Stay organized with collections Save and categorize content based on your preferences.

To view an aggregate representation of your trace data, or to find and explore
individual traces or traces that contain specific labels, use the
**Trace Explorer** page.

The following screenshot illustrates how trace data is shown:

![Example display of trace data.](/static/trace/images/trace-explorer-example.png)

To run queries that perform an aggregate analysis of your spans, use the
**Log Analytics** page or BigQuery. Both interfaces support querying
your span data by using SQL. When you use the **Log Analytics** page, you can
view query results as a table or as a chart. To learn more about using
SQL to query your trace data, see
[Query and analyze traces](/trace/docs/analytics).

This feature is supported only for Google Cloud projects.
For [App Hub](/app-hub/docs/overview)
configurations, select the App Hub host project or management project.

## About the **Trace Explorer** page

To help you identify trends and patterns in your trace data, the latency data
is aggregated and displayed in charts. The heatmap uses color to represent
the number of spans in a cell. A cell with many spans has a darker color than
one with few spans. Each cell's tooltip displays latency and other information.
You can also view latency percentiles and span rate information.

When you are investigating an issue, you might want to view a specific trace
or only spans with certain properties:

* To restrict which spans are shown, [apply filters](#filter_traces). For
  example, you can filter by service, application, error state, and other
  properties.
* To display a specific trace, use the toolbar's
  click *pageview* **Search for trace** option.

To identify outliers and view details of individual spans, use the tabular
section:

* You can sort the rows of the **Spans** and **Grouped** tabs by the duration
  header.
* To understand how many spans different services are generating, use the
  **Grouped** tab. Each row corresponds to a service and span name, and
  for each entry, latency statistics are shown.

To explore details of a span or grouping, select the entry from a row in the
tabular section. A flyout opens that displays the span in the context of its
trace. From this view, you can explore the span, its attributes, and view events
and log data. You also can
[search the spans and attributes in the trace for keywords](#search-trace).

The trace data that the **Trace Explorer** page depends on the
following:

* The projects searched for trace data. By default, the system only searches
  the project selected by the project picker for trace data. However, you can
  configure the page to search the list of projects in a
  [trace scope](/trace/docs/trace-scope/create-and-manage).
* Your Identity and Access Management (IAM) permissions on the searched projects.
  If you don't have the permission to view trace data for a project, then
  the Google Cloud console displays a warning message and the data from that
  project isn't displayed.
* The time-range setting.
* The filters you apply.

The remainder of this page provides more information about how to find and
explore your trace data.

## Before you begin

To get the permissions that
you need to view trace data by using the Google Cloud console and to or select a trace scope,
ask your administrator to grant you the
[Cloud Trace User](/iam/docs/roles-permissions/cloudtrace#cloudtrace.user)  (`roles/cloudtrace.user`)
IAM role on your project.
For more information about granting roles, see [Manage access to projects, folders, and organizations](/iam/docs/granting-changing-revoking-access).

This predefined role contains
the permissions required to view trace data by using the Google Cloud console and to or select a trace scope. To see the exact permissions that are
required, expand the **Required permissions** section:

#### Required permissions

The following permissions are required to view trace data by using the Google Cloud console and to or select a trace scope:

* To select a trace scope:
  `cloudtrace.traceScopes.[get, list]`
* To read the default trace scope:
   `observability.scopes.get`

You might also be able to get
these permissions
with [custom roles](/iam/docs/creating-custom-roles) or
other [predefined roles](/iam/docs/roles-overview#predefined).

For more information about roles, see
[Control access with Identity and Access Management](/trace/docs/iam).

## View aggregated trace data

To view the aggregated information about your trace data, do the following:

1. In the Google Cloud console, go to the
   ![](/static/stackdriver/images/trace-explorer-icon.png)
   **Trace explorer** page:

   [Go to **Trace explorer**](https://console.cloud.google.com/traces/explorer)

   You can also find this page by using the search bar.

   It might take several minutes after the
   first trace data is written
   to a Google Cloud project before that data is available to view.
   If you don't see any trace data displayed after waiting a few minutes, then
   your project might not have any data to display or there might be a
   configuration issue. For information about how to resolve these issues, see
   [Troubleshoot: No data in the Trace interface](/trace/docs/troubleshooting#no-data-refresh).
2. Configure the **Trace Explorer** page:

   1. In the toolbar of the Google Cloud console,
      select your Google Cloud project. For [App Hub](/app-hub/docs/overview)
      configurations, select the App Hub host project or management project.
   2. Optional: Configure
      which projects are searched for trace data by using the **Scope** element:

      * To show the trace data that is stored in your project, set the
        first menu of the **Scope** element to
        ![](/static/stackdriver/images/gc-project-icon.png) **Project** or to ![](/static/stackdriver/images/trace-scope-icon.png) **\_Default**.
        These two settings are equivalent.
      * To show the trace data that is stored in multiple projects, expand the
        first menu of the **Scope** element, select
        **Trace scope**, and then select the trace scope that lists
        those projects. After you make your selection, the **Scope** menu displays
        a trace scope icon, ![](/static/stackdriver/images/trace-scope-icon.png), and the name of the
        selected trace scope.

      The data that is returned depends on your
      IAM roles on the searched projects. For example, the
      searched projects include a Google Cloud project that you don't have
      access to, then no trace data for that project is returned.

      For more information, see
      [Create and manage trace scopes](/trace/docs/trace-scope/create-and-manage).
   3. Optional: Update the time range by using the time-range selector or by
      using your pointer to highlight a range on the x-axis.

      For example, you might set this selector to **Last 2 weeks** when you want
      to see whether there are any trends in the latency data.
      Span data is stored for 30 days.
3. Explore the heatmap:

   * Use color to identify trends and outliers. A cell with many spans has a
     darker color than one with few spans.
   * View details of the cell by using the cell's tooltip. The tooltip lists
     number of spans, date and time, and the time interval of the cell.

     **Note:** If you select a cell in the heatmap, then the table that lists
     individual spans or groupings of spans is updated.
4. Explore latency percentiles and error rates:

   * To view latency trends, set the **Chart view** menu to
     **Span duration (percentile)**.
     The duration chart displays the 50th, 90th, 95th, and 99th percentiles.
   * To view the response status as a function of time,
     set the **Chart view** menu to **Span rate**. The chart displays the
     rate of spans being sent to your project.
5. Use the **Spans** and **Grouped** tables to identify outliers or to view
   statistical information. The **Spans** table lists individual spans. The
   **Grouped** table groups spans by their name and by service or workload name.

   * To view outliers or find a span name, sort the table. You can sort by
     any column header.

     For example, sorting the **Spans** table by duration lets you find
     spans with high latency.
   * To view statistics like average latency, use the **Grouped** table.
   * To find App Hub-registered services and workloads, search
     the **Service/workload** column for entries that include the
     service icon, ![](/static/stackdriver/images/app-hub-service-icon.png), or the
     workload icon, ![](/static/stackdriver/images/app-hub-workload-icon.png).
     The link provided with an App Hub-registered
     service or workload opens the corresponding Application Monitoring dashboard.

   If you want more information about a particular grouping, then select the
   span name for a row. A flyout opens that displays the span in the context of
   its trace. You can then [explore the span and trace](#explore).
6. To restrict which spans are shown, add filters.
   To learn more about filtering your trace data, see the next section.

## Filter your trace data

To display only information that is of interest to you, apply filters.
Filters restrict what data is shown. For example, you might
filter by service name and by status. Or, if you've deployed applications
to [App Hub](/app-hub/docs/overview), you might want to view the trace data
only for the application, or for a specific service or workload that is part
of the application.

When you add or remove a filter, the data displayed by the
**Trace Explorer** page is refreshed and
only shows those spans that match all applied filters.

### Filter by a trace by ID

When you are troubleshooting an incident or failure, you might know the
trace ID. To explore that trace, go to the toolbar,
click *pageview* **Search for trace**,
and enter the [trace ID](/trace/docs/reference/v1/rest/v1/projects.traces#Trace).

When you enter a valid ID, the **Details** flyout opens and displays
information about the trace and its spans. You can use the options in that
pane to explore the trace. For example, you might
[search the spans for keywords](#search-trace).

**Note:** If you enter a trace ID that isn't found, then the trace data might be
stored in a project that isn't searched by the
**Trace Explorer** page,
or you might not have an IAM role that lets you
view trace data. To resolve these failures, identify the projects that
store the trace data. For each project, verify that your
IAM role lets you view trace data and then ensure that the
**Scope** element is configured to search all
projects that store your trace data. For more information, see
[Update the list of projects searched for trace data](#refine-scope).

### Apply span filters

The **Span filters** pane lists the most common filters. You can select
multiple entries from any subcategory. As you add or remove filters,
the **Filter** bar is also updated.

The values for all menus are derived from your trace data. When a menu includes
an option without any text, that option refers to spans that don't
include the corresponding attribute.

The following **Span filters** are typically available:

* **OpenTelemetry service**: Filters by the `service.name` attribute.
* **Span name**: Name of the span.
* **Span status**: The request status. For information about the values,
  see the [OpenTelemetry SpanStatus documentation](https://opentelemetry.io/docs/concepts/signals/traces/#span-status).
* **Duration**: The duration of the span.
* **Span kind**: Describes the relationships between spans. For information
  about the values, see the [OpenTelemetry SpanKind documentation](https://opentelemetry.io/docs/concepts/signals/traces/#span-kind).
* **App Hub application**: Filters by the `gcp.apphub.application.id`
  resource attribute.
* **App Hub service**: Filters by the `gcp.apphub.service.id`
  resource attribute.
* **App Hub workload**: Filters by the `gcp.apphub.workload.id`
  resource attribute.

If you want to filter by an attribute that isn't listed in the
**Span filters** pane, then use the **Filter** bar.

### Use the filter bar

The **Filter** bar lets you apply a filter with a predefined filter key and
a value that you select, or you can enter both the key and value.

To add a filter, select **Add filter**, and then do one of the following:

* Select a defined key, like **Span name**, and then select a value from
  the secondary menu.
* Select **Add attribute filter**, and then add your custom key and value.
  If you enter your own filter key, then use the same syntax as a key for an
  attribute on a span.

  For example, to filter by the host identifier, set the key to `host.id`.
  Similarly, to filter by status code, set the key to `/http/status_code`.
  In this scenario, you might set the value to `200`, which results in the
  filter `/http/status_code: 200`.
  To let the filter match any value, select **Any value**.

### Filter by application

To find or view spans your [App Hub](/app-hub/docs/overview)-registered services and
workloads generate, your spans must contain the following resource attributes:

* `gcp.apphub.application.{container,id,location}`
* `gcp.apphub.{workload,service}.{criticality_type,environment_type,id}`

The previous resource attributes are generated by
[instrumentation that you add to your applications](/monitoring/docs/instrument-for-application-monitoring).
You can filter your trace data by any resource attribute.
However, the following **Span filters** filter by the application, service,
and workload IDs:

* **App Hub application**
* **App Hub service**
* **App Hub workload**

To open the Application Monitoring dashboard for a
App Hub-registered service and workload, do the following:

1. Go to the **Spans** or **Grouped** table and find the service or
   workload. You might look for the service icon, ![](/static/stackdriver/images/app-hub-service-icon.png),
   the workload icon, ![](/static/stackdriver/images/app-hub-workload-icon.png), or filter the table.
2. Select the link in the **Service/workload** column.

## Explore a trace

This section provides information about how you can explore a span in the
context of its trace:

1. Open and configure the **Trace Explorer** page. For information
   about these steps, see [View aggregated trace data](#view-recent).
2. To view details of a span or a trace, do one of the following:

   * Go to the table section of the **Trace Explorer** page and
     select an entry from the tabular section. You can sort the rows of the
     tables by any table header. You can [apply filters](#filter_traces) to
     restrict which spans the tables show.
   * Go to the toolbar of the **Trace Explorer** page,
     click *pageview* **Search for trace**,
     and enter the [trace ID](/trace/docs/reference/v1/rest/v1/projects.traces#Trace).

   The **Details** flyout opens and displays a trace and its spans.

   ![Example of the trace flyout.](/static/stackdriver/images/trace-flyout-example.png)

   The details for the span or trace you selected are shown:

   * The **Name** column displays the call hierarchy and the first entry
     includes the trace ID. This column might also include annotations that
     indicate whether generative AI events or log data is available.
   * The **Service/workload** column displays a service or workload name.
     Service names are extracted from the
     OpenTelemetry attribute `service.name`, when that attribute is set.
     If that attribute isn't set and if the service is running on
     App Engine, then the App Engine service name is
     displayed. Otherwise, no service is specified.
   * The length of the latency bar is representative of the latency value.
   * The color of the latency bar indicates status. A blue latency bar indicates
     a successful completion while a red latency bar indicates an error occurred.
   * A circle on a latency bar indicates a log entry or event is associated with
     the span. To change this behavior, use the **Logs & events** menu.
3. To explore the trace, do the following:

   * Use your pointer to select different spans. When you select a span, the
     tabs on the page are refreshed to show the span's
     [attributes, log entries, and events](#attributes-events).
   * To search the spans in the trace for keywords,
     use the **Find in Trace** field.

     Search applies only to the span name, service or workload name,
     and attributes fields.
     You can only search by plain text, and you can't search logs, events, or
     metadata.

     For example, if you enter `GET`, then text in the **Name**,
     **Service/workload**, and **Attributes** panes that displays `GET`,
     ignoring case, is highlighted.

### View attributes, log entries, and events

The **Details** flyout for a span contains a tab for each of the following:

* **Attributes**: This tab lists labels that are attached to spans.
  For information about labels, see [Trace labels](/trace/docs/trace-labels).
* **Logs & Events**: This tab lists events and log entries whose
  `trace_id` and `span_id` fields match the selected span are shown. Only
  log entries that you have permission to view are shown.

  To explore an entry on this tab,
  click *keyboard\_arrow\_down* **Show more**.

  If you prefer to use the Logs Explorer page to view log data, then
  click **View logs**. The query is set to filter to a specific trace, span,
  and time range.

  **Note:** Generative AI events are shown on the **Inputs/Outputs**
  tab. To learn more, see [View generative AI events](#generative-events).
* **Stacktraces**: Lists the available stacktraces.
* **Metadata & Links**: Lists general information about the span:

  + Span ID: The span ID is a 64-bit integer other than 0. For details, see
    [`TraceSpan`](/trace/docs/reference/v1/rest/v1/projects.traces#TraceSpan).
  + Parent span ID.
  + Project ID.
  + Start time and end time.
  + Table that lists links to other spans. For each link, this table lists
    the following:

    - The key-value pairs for the linked-to span.
    - The trace ID for the linked-to-span. When this field lists
      **Current trace**, then the span is linking to another span in the
      same trace.

    For information about links, see the
    [`Links`](/trace/docs/reference/v2/rest/v2/Links) API reference page.

The **Details** might also include a tab labeled
**Inputs/Outputs** tab. This tab displays generative AI events.

### View generative AI events

**Preview**

This feature is
subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
[Service Specific
Terms](/terms/service-terms#1).
Pre-GA features are available "as is" and might have limited support.
For more information, see the
[launch stage descriptions](https://cloud.google.com/products/#product-launch-stages).

To view events related to generative AI agents, use the
**Inputs/Outputs** tab. This tab displays events that follow
the [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions/tree/v1.37.0/docs/gen-ai).

There are two supported configurations:

* Text-based prompts and responses that are attached to the spans as
  [*attributes*](https://opentelemetry.io/docs/specs/otel/common/#attribute), which are key-value pairs that describe some
  characteristic or an event. For example, the value for the key
  `gen_ai.system` identifies the system that provides the generative AI
  capabilities. The keys for generative AI attributes begin with `gen_ai`.
* Multimodal prompts and responses that are stored in a
  Cloud Storage bucket. Cloud Trace identifies these events by
  correlating your trace and log data. To learn about supported
  configurations, see
  [Collect and view multimodal prompts and responses](/trace/docs/collect-view-multimodal-prompts-responses).

The following screenshot illustrates how the **Trace Explorer**
page renders text-based generative AI events that are attached to the spans:

![Display of trace spans.](/static/stackdriver/docs/instrumentation/images/trace-explorer-langgraph-ai-events.png)

To learn about the sample application that generated the previous screenshot,
see [Instrument a LangGraph ReAct Agent with OpenTelemetry](/stackdriver/docs/instrumentation/ai-agent-langgraph).

## What's next

* [Create and manage trace scopes](/trace/docs/trace-scope/create-and-manage)
* [Share traces and spans](/trace/docs/share-trace-or-span)
* [Troubleshoot](/trace/docs/troubleshooting)

Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-19 UTC.

Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-03-19 UTC."],[],[]]
