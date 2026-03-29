---
title: New Blog Infrastructure
---
So, welcome to my new blog.

But, Why New Blog?
-----

There are few reasons:
* I need more control on writing the blog.
* I want something where I can just write in Markdown.
* I want blog where I have both local and remote copy of my blog post.

Unfortunately, Blogger, [where my old blog is hosted on](https://auahdark687291.blogspot.com), doesn't satisfy that
criteria.

But isn't Blogger Has More Features?
-----

Of course. Blogger currently has its advantages:
* Tagging system
* Post categorization
* Better SEO

But I believe with the current engine, those can be implemented later.

How New Blog Works?
-----

### Trivial Explanation

The blog uses Python, GitHub Actions, and GitHub Pages for its whole infrastructure. Basically:
* Python script to generate all the post pages and the index.html
* GitHub Actions used to run the Python script in CI.
* GitHub Pages deploys it to the web.

### Technical Explanation

#### Blog Repository

The [blog repository](https://github.com/MikuAuahDark/blog) is where all the markdown files (blog post) are stored.
It's set up such that pushing new `.md` (and only `.md`) files triggers page rebuild. It has 3 branches:
* `master` - Where the blog assets and renderer files are placed. Despite the branch name, I do not support slavery!
* `metadata` - Date time information about each blog post.
* `gh-pages` - Deployed page, using GitHub Pages.

If you look on the `master` branch, there will be these files:
* `assets` - Static assets, placed in `assets/` ono the deployed GH Pages.
* `renderer` - Jinja2 templating engine used on how to render the index page of the blog and each page.
  * `render_page.py` expose single `render` Python function using `page.html` as template. This generates HTML for a
    blog post.
  * `render_index.py` expose single `render` Python function using `index.html` as template. This generates HTML for
    the main page, e.g. opening <https://mikuauahdark.github.io/blog>.
* The `*.md` files - The actual blog post. Each blog post must have YAML front matter with at least `title` element.
  If you look on the source of this blog post markdown, you may note there's only `title`, while the others (like
  [SIF Note Handling](sif1-note-handling.html)) also has `original-date`. The `original-date` is used to mark that the
  original blog post is actually written in the past. If no `original-date` is present, the blog post date is
  automatically deducted by the commit date where this file is added/modified.

One thing to remember that it explicitly only look for blog post with extension of `.md`, not `.markdown`. This is
important to make sure the README and LICENSE of the blog repository is skipped.

#### Blog Engine

Now files in `renderer` cannot stand on its own. That's why there's called
["blog engine"](https://github.com/MikuAuahDark/blog-engine). Blog engine has single script `main.py` which handles
most of the thing:
* HTML generation by invoking the blog repository's `renderer` scripts.
* Metadata modification
* Post date calculation, and modify last update.

#### Workflow

The GitHub Actions workflow is as follows:
1. Checkout the "blog engine" repository.
2. Checkout the blog repository on all 3 branches: `master`, `metadata`, and `gh-pages`. It's checked out on `content`,
   `metadata`, and `gh-pages` folder respectively.
3. It setups the Python, install the needed requirements both for the blog engine and the repository.
4. It then run the `main.py` script.
5. Copy all `assets/` from `content/assets` to `gh-pages/assets`, using `content` one as SSOT.
6. It then commits changes both in `metadata` and `gh-pages`.
7. Changes in `gh-pages` will be automatically detected by GitHub Pages deployment.

Honestly, just check the repo. I probably explain these things poorly.

What About Other SSG?
-----

Honestly I'm not aware of it and the learning curve is probably not straightforward for me. My idea is having blog
where posting is as simple as making Markdown file, `git commit`, then `git push`. Then, the post date is
automatically deducted from the commit date instead of having to type it manually. Isn't that just awesome?

---

So yeah, checkout this blog repository at <https://github.com/MikuAuahDark/blog>. The blog content is licensed under
Creative Commons Attribution 4.0 unless I state it otherwise. the blog engine at
<https://github.com/MikuAuahDark/blog-engine> is licensed under permissive MIT license.

I'll bring more blog posts from Blogger to here when I have more free time.
