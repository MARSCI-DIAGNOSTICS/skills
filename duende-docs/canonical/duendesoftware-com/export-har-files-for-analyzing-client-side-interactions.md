---
title: Export HAR Files for Analyzing Client-Side Interactions
source_url: https://docs.duendesoftware.com/export-har-files-for-analyzing-client-side-interactions/
source_type: llms-full-txt
content_hash: sha256:f0751726d2141284411bade45e85ad83be14791e4b095dc3b4a2a370078b2315
doc_id: export-har-files-for-analyzing-client-side-interactions
---

> Documentation for creating HAR files, and how they can be used for client-side diagnostics.

[HTTP Archive (HAR)](https://en.wikipedia.org/wiki/HAR_\(file_format\)) files are logs of network interactions made by a web browser. They contain headers, request bodies, response payloads, and even sensitive information like cookie values sent and received for each interaction.

Do not share sensitive information

Before sharing HAR files you should ensure they do not contain any sensitive information. You can sanitize a file by following the [steps below](#sanitize-a-har-file).

## When To Use A HAR File

[Section titled "When To Use A HAR File"](#when-to-use-a-har-file)

Because HAR files are traces of all network interactions within the browser, they are commonly shared with another party to help diagnose issues. A common scenario is when there are multiple services involved with a use case. You can imagine an application where a user logs in to a site with Duende IdentityServer on the backend, and an external IdP storing the user account. That scenario has three distinct applications and the HAR file is used to trace if/when certain cookies are set within the login flow.

## HAR File Considerations

[Section titled "HAR File Considerations"](#har-file-considerations)

* Consider using an **incognito window** of your browser.
  * If you do, close all browser incognito instances you may have open and then open a new window to ensure the cache is cleared.
* Preserve the log across page navigation.
  * If you are navigating to different pages (ex: logging in to a site with OAuth redirects), then any network calls made before the last redirect will be lost. Preserving the logs across page navigation aids in diagnosing issues. The below steps include instructions to preserve network logs while navigating across multiple pages.
* Generate HAR files with sensitive data.
  * It is helpful to know that certain fields are have been set, but not necessarily the actual value. Some browsers will exclude sensitive data in HAR file exports by default. The below steps include instructions to enable sensitive data in HAR file exports for browsers that do not include it by default.

## Generating A HAR File

[Section titled "Generating A HAR File"](#generating-a-har-file)

Generating a HAR file involves steps using your web browser and its associated developer tools. The browser-specific steps outlined below are all similar to each other. Other browsers will have similar steps.

### Google Chrome

[Section titled "Google Chrome"](#google-chrome)

1. Open the browser dev tools <https://developer.chrome.com/docs/devtools/open>.
2. In the dev tools, click on the Settings icon. Under the Network category, enable "Allow to generate HAR with sensitive data".
3. In the dev tools, navigate to the Network tab and enable the "Preserve log" checkbox.
4. In the browser, visit the page(s) and perform the steps that trigger the issue.
5. In the Network tab of the dev tools, click the down arrow and select the "Export HAR (with sensitive data)..." option to export the HAR file and save it locally.

### Safari

[Section titled "Safari"](#safari)

1. Enable the Web Inspector, and open it <https://developer.apple.com/documentation/safari-developer-tools/enabling-developer-features>.
2. In the Web Inspector in the Developer menu, navigate to the Network tab. Click the "Filter" button and enable "Preserve Log".
3. In the browser, visit the page(s) and perform the steps that trigger the issue.
4. In the Web Inspector, click "Export" to export the HAR file and save it locally.

### Firefox

[Section titled "Firefox"](#firefox)

1. Open the browser dev tools <https://firefox-source-docs.mozilla.org/devtools-user>.
2. In the dev tools, navigate to the Network tab, click the Network Settings icon, and enable "Persist Logs".
3. In the browser, visit the page(s) and perform the steps that trigger the issue.
4. In the Network tab of the dev tools, click the Network Settings icon, and select "Save All As Har" to save it locally.

### Microsoft Edge

[Section titled "Microsoft Edge"](#microsoft-edge)

1. Open the browser dev tools <https://learn.microsoft.com/en-us/microsoft-edge/devtools/overview>.
2. In the dev tools, click on the ellipsis icon, then select "Settings". Under the Network category, enable "Allow to generate HAR with sensitive data".
3. In the dev tools, navigate to the Network tab and enable the "Preserve log" checkbox.
4. In the browser, visit the page(s) and perform the steps that trigger the issue.
5. In the Network tab of the dev tools, click the down arrow and select the "Export HAR (with sensitive data)..." option to export the HAR file and save it locally.

## Viewing A HAR File

[Section titled "Viewing A HAR File"](#viewing-a-har-file)

HAR files are JSON files with a specific file extension. You can open one with any text editor you would normally open JSON files with. You can also import the HAR file into your browser dev tools to visualize it the same way you could see network interactions before exporting the file.

## Sanitize A HAR File

[Section titled "Sanitize A HAR File"](#sanitize-a-har-file)

Before sharing your HAR file with anyone, you should remove any sensitive data. You can do this manually by opening the HAR file with any JSON text editor and removing the sensitive data. We recommend replacing the data with a placeholder rather than deleting the entry. When diagnosing issues, it's helpful to know whether a field was set.

## Practice

[Section titled "Practice"](#practice)

If you would like to practice with a small sample, you can login to the Duende Demo Server and generate a HAR file from those interactions.

1. In your browser, navigate to <https://demo.duendesoftware.com/Account/Login>.
2. With your browser and dev tools open, the log being preserved, and the ability to export a HAR file with sensitive data, login to the site using one of the built-in users.
3. Export the HAR file with sensitive data.
4. Explore the HAR file JSON with a text editor or import it into your browser dev tools.
