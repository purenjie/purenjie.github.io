# CHANGELOG

Base on Hugo Theme Puppet [commit 71e55a8](https://github.com/roninro/hugo-theme-puppet/tree/71e55a893702ea6e1a15a71a3d0e2248673794f1), the changes made are listed below:
* delete folder `exampleSite\` and `images\`
* delete file `netlify.toml`
* delete images:
  * `static\favicon.ico`
  * `static\img\`
* Modify Area Sidebar Bio to let it have ability to fit multi-line bios, related to files:
  * `assets\sass\_sidebar.scss`
  * `layouts\partials\short-about.html`
* To fix the iOS phone search issue, update the version of [Simple-Jekyll-Search](https://www.npmjs.com/package/simple-jekyll-search) to locally dev bundle version 1.10.0
* Remove the `zoom.js` related code, and replace it with `lightbox2`:
  * delete:
    * `assets\zoomjs\` 
  * add:
    * `static\css\lightbox.min.css`
    * `static\images\`
    * `static\js\lightbox.min.js`
  * modify:
    * `layouts\baseof.html`
    * `layouts\footer.html`
    * `layouts\render-image.html`
* Replace the font-awesome cdn version to local
  * add:
    * `static\css\fontawesome-free@all.min.css`
    * `static\webfonts\`
  * modify:
    * `layouts\baseof.html`
* Modify `assets\sass\main.scss` to let code part scrollbar more beautiful
