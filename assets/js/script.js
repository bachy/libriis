jQuery(document).ready(function($) {

  console.log("Hello Les notices");

  // $('.story-page').each(function(index, el) {
  //   $figures = $('figure', this);
  //   $(this).addClass("figures-"+$figures.length);
  // });

  $('.story-page-2 h2, .story-page:not(.story-page-0):not(.story-page-1):not(.story-page-2) h1').each(function(index, el) {
    // console.log("item to typotize",$(this).text());
    var chars = $(this).text().split("");
    // console.log("chars", chars);
    var typotized = "";
    var k = 0;
    for (var j = 0; j < chars.length; j++) {
      // console.log('node '+j+" modulo : "+(j % 6),chars[j]);
      if(! /\s/.test(chars[j]) ){
        k++;
        if ( k % 12 == 0){
          typotized += '<span class="typo-4">'+chars[j]+'</span>';
          continue;
        }
        if ( k % 9 == 0){
          typotized += '<span class="typo-3">'+chars[j]+'</span>';
          continue;
        }
        if ( k % 6 == 0){
          typotized += '<span class="typo-2">'+chars[j]+'</span>';
          continue;
        }
        if ( k % 3 == 0){
          typotized += '<span class="typo-1">'+chars[j]+'</span>';
          continue;
        }
      }
      typotized += chars[j];
    }
    $(this).html(typotized);
  });

/*
  // Detect if a flow element is in odd or even paper

  // var flow = document.webkitGetFlowByName('flow-main');
  // var flow = NamedFlowMap;//();//getFlowByName("flow-main");
  // console.log('flow', window);
  var namedFlow = document.webkitGetNamedFlows()["flow-main"];
  console.log(namedFlow);
  // var regions = namedFlow.getRegions();
  // var content = namedFlow.getContent();

  setTimeout(function(){
    var region, paper, paperid;
    $(".story-page>h1,.story-page>figure", "#flow-main").each(function(index, el) {
      region = namedFlow.getRegionsByContent(this);
      // paper = $(region).parents('.paper');
      paperid = $(region).parents('.paper').attr('id').match(/page-(\d+)/)[1];
      // console.log(paperid);
      if(paperid % 2 == 0){
        $(this).addClass('paper-odd')
      }else{
        $(this).addClass('paper-even')
      }
    });
  }, 1000);
*/
});
