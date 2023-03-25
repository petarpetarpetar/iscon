(function ($) {
  $.fn.countTo = function (options) {
    options = options || {};

    return $(this).each(function () {
      // set options for current element
      var settings = $.extend(
        {},
        $.fn.countTo.defaults,
        {
          from: $(this).data("from"),
          to: $(this).data("to"),
          speed: $(this).data("speed"),
          refreshInterval: $(this).data("refresh-interval"),
          decimals: $(this).data("decimals"),
        },
        options
      );

      // how many times to update the value, and how much to increment the value on each update
      var loops = Math.ceil(settings.speed / settings.refreshInterval),
        increment = (settings.to - settings.from) / loops;

      // references & variables that will change with each update
      var self = this,
        $self = $(this),
        loopCount = 0,
        value = settings.from,
        data = $self.data("countTo") || {};

      $self.data("countTo", data);

      // if an existing interval can be found, clear it first
      if (data.interval) {
        clearInterval(data.interval);
      }
      data.interval = setInterval(updateTimer, settings.refreshInterval);

      // initialize the element with the starting value
      render(value);

      function updateTimer() {
        value += increment;
        loopCount++;

        render(value);

        if (typeof settings.onUpdate == "function") {
          settings.onUpdate.call(self, value);
        }

        if (loopCount >= loops) {
          // remove the interval
          $self.removeData("countTo");
          clearInterval(data.interval);
          value = settings.to;

          if (typeof settings.onComplete == "function") {
            settings.onComplete.call(self, value);
          }
        }
      }

      function render(value) {
        var formattedValue = settings.formatter.call(self, value, settings);
        $self.html(formattedValue);
      }
    });
  };

  $.fn.countTo.defaults = {
    from: 0, // the number the element should start at
    to: 0, // the number the element should end at
    speed: 1000, // how long it should take to count between the target numbers
    refreshInterval: 100, // how often the element should be updated
    decimals: 0, // the number of decimal places to show
    formatter: formatter, // handler for formatting the value before rendering
    onUpdate: null, // callback method for every time the element is updated
    onComplete: null, // callback method for when the element finishes updating
  };

  function formatter(value, settings) {
    return value.toFixed(settings.decimals);
  }
})(jQuery);

jQuery(function ($) {
  // custom formatting example
  $(".count-number").data("countToOptions", {
    formatter: function (value, options) {
      return value
        .toFixed(options.decimals)
        .replace(/\B(?=(?:\d{3})+(?!\d))/g, ",");
    },
  });

  // start all the timers
  $(".timer").each(count);

  function count(options) {
    var $this = $(this);
    options = $.extend({}, options || {}, $this.data("countToOptions") || {});
    $this.countTo(options);
  }
});

function changeHandler() {
  var value =
    "=" + String(document.getElementById("valueselect").value) + ".00 BAM";
  document.getElementById("moneyamount").value = value;
}

function submitButtonHandler() {
  var racunPrimaoca = document.getElementById("racunPrimaoca").value;
  var razlogPlacanja =
    document.getElementById("valueselect").options[
      document.getElementById("valueselect").selectedIndex
    ].text;
  var kolicinaNovca = document.getElementById("valueselect").value;
  var samofinansiranje = false;
  if (document.getElementById("samofinansiranje").checked) {
    samofinansiranje = true;
  }

  const xhr = new XMLHttpRequest();
  alert([racunPrimaoca, razlogPlacanja, kolicinaNovca, samofinansiranje]);
  //   xhr.addEventListener("readystatechange", function () {
  //     if (this.readyState === this.DONE) {
  //       console.log(this.responseText);
  //       if (this.status === 200) {
  //         location.replace(`/studentProfil`);
  //       } else if (this.status === 401) {
  //         alert(JSON.parse(this.response)["Message"]);
  //       }
  //     }
  //   });

  xhr.open("POST", `/paymentSlip`);
  xhr.setRequestHeader("Content-Type", "application/json");
  data = JSON.stringify({
    racunPrimaoca: racunPrimaoca,
    svrhaUplate: razlogPlacanja,
    kolicinaNovca: kolicinaNovca,
    samofinansiranje: samofinansiranje,
  });

  xhr.send(data);
  //   // location.href = 'http://192.168.137.80:5000/login'
}
