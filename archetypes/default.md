
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: ""  # desc of series / summary of post / delete to summary from post content
subtitle: ""  # can be deleted
header_img: "/img/.jpg"  # can be deleted
short: true
toc: true
tags: []
series: ["tech", "think"]  # should be ONLY ONE of the ["tech", "think"]
slug: "{{ .Date | time.Format "20060102" }}-title-url"  # final real url, recommend: start by date, follow lower case words with hyphen splitter. E.g., `20230316-text-title`
---
