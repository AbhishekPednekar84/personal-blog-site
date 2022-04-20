Title: Google Analytics 4 with Next.js
Date: 2022-04-20 21:00
Category: Next.js
Tags: Next.js
Slug: next-ga4
Authors: Abhishek Pednekar
Summary: Enable Google Analytics 4 in a Next.js website
Description: Enable Google Analytics 4 in a Next.js website
Cover: /static/images/nextjs.jpg

Recently, Google announced that Universal Analytics (UA) would be sunset on July 1st, 2023. Post this date, UA would not process any new hits. The data collected by UA would be available for six months thereafter. Google has strongly recommended individuals and businesses using the UA property switch to their new analytics measurement solution, **Google Analytics 4**.

In this article, we will see how Google Analytics 4 can be integrated with a Next.js website. The article assumes that the reader has a Google Analytics account and is familiar with Next.js.

## Creating a Google Analytics 4 property

On the **Admin** section of your Google Analytics dashboard, click on the **Create Property** button. This by default will create a Google Analytics 4 property.

![ga4-create-property]({static}/images/index27/next-ga4-1.jpg)

<br />
Once you enter basic information like the property name and work details, you will be prompted to create a data stream. Click on **Web** to generate the site tag for your Next.js website.

![ga4-create-stream]({static}/images/index27/next-ga4-2.jpg)

<br />
You will now see the code you need to embed in your website in the **Tagging instructions** section.

![ga4-tag-details]({static}/images/index27/next-ga4-3.jpg)

<br />
## Embedding the site tag in Next.js

**Step 1**: Create an environment variable with the Google Analytics 4 measurement id.

```
// .env.local

NEXT_PUBLIC_GA4_MEASUREMENT_ID="G-xxxxxxxx"

```

<br />
**Step 2**: Create a `_document.js` file in the `pages` directory (if not already present) to add the tracking code. `_document.js` overrides the default document provided by Next.js.

```
// _document.js

import Document, { Html, Head, Main, NextScript } from "next/document";

class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>
          <script
            async
            src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID}`}
          />
          <script
            dangerouslySetInnerHTML={{
              __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID}', {
              page_path: window.location.pathname,
            });
          `,
            }}
          />
        </Head>

        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;

```

<br />
**Step 3**: Finally, in `_app.js`, we will use the `useEffect` hook and the `routeChangeComplete` event provided by the Next.js `router` to run the analytics code when a route changes. We will subscribe to the `routeChangeComplete` event whenever the component mounts and unsubscribe on unmount.

```
import { useEffect } from "react";

function MyApp({ Component, pageProps, router }) {

  useEffect(() => {
    const handleRouteChange = (url) => {
      window.gtag("config", process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID, {
        page_path: url,
      });
    };

    // Subscribe to the change event
    router.events.on("routeChangeComplete", handleRouteChange);

    return () => {
      router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, [router.events]);

 return <Component {...pageProps} />
  );
}

export default MyApp;

```

That's it! Refresh your page a couple of times to see the activity on your Google Analytics dashboard.

### Further reading

<i class="fas fa-book-open"></i> This article is inspired by a [post](https://mariestarck.com/add-google-analytics-to-your-next-js-application-in-5-easy-steps/) from Marie Starch<br />
<i class="fas fa-book-open"></i> Next.js [custom document](https://nextjs.org/docs/advanced-features/custom-document)<br />
<i class="fas fa-book-open"></i> Next.js [router events](https://nextjs.org/docs/api-reference/next/router#routerevents)
