<link rel="stylesheet" class="aplayer-secondary-style-marker" href="/assets/css/APlayer.min.css"><script src="/assets/js/APlayer.min.js" class="aplayer-secondary-script-marker"></script>hexo.extend.tag.register('mood', function(args, content){
	date = args[0]
	time = args[1]
	logo = args[2]
	var result = '';
	result += '<blockquote>';
	logo = '<span class="fa-stack fa-lg"><i class="fa ' + logo + ' fa-stack-1x"></i></span>';
	result += hexo.render.renderSync({text: logo + content, engine: 'markdown'});
	footer = '<span>' + date + ' ' + time + '</span>'
	result += '<footer>' + footer + '</footer>';
	result += '</blockquote>';
	return result;
}, {ends: true});<script>
        document.querySelectorAll('.github-emoji')
          .forEach(el => {
            if (!el.dataset.src) { return; }
            const img = document.createElement('img');
            img.style = 'display:none !important;';
            img.src = el.dataset.src;
            img.addEventListener('error', () => {
              img.remove();
              el.style.color = 'inherit';
              el.style.backgroundImage = 'none';
              el.style.background = 'none';
            });
            img.addEventListener('load', () => {
              img.remove();
            });
            document.body.appendChild(img);
          });
      </script>