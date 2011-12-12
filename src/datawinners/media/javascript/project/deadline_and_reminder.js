//All the deadline related drop-downs. They are very very very annoying.
DW.DeadlineDetails = function(){
    this.deadlineSectionSelectControls = '#frequency_values select';
    this.deadlineEnabledControl = 'input[name=has_deadline]';
    this.deadlineEnabledCheckedControl = 'input[name=has_deadline]:checked';
    this.frequencyPeriodControl = 'select[name=frequency_period]';
    this.deadlineTypeControl = 'select[name=deadline_type]'; //For the control which lets user select Same and Following. I wish i had a better name for this one.
    this.deadlineMonthControl = 'select[name=deadline_month]';
    this.deadlineWeekControl = 'select[name=deadline_week]';
    this.month_block_class = '.month_block';
    this.week_block_class = '.week_block';
    this.reminders_block_id = '#reminders_section';
};

DW.DeadlineDetails.prototype = {
    init: function(){
        //var is_deadline_enabled = ($(this.deadlineEnabledCheckedControl).val() === "True");
        //if(is_deadline_enabled){
            this.show();
        //}else{
          //  this.hide();
       // }
        return true; //It's a Best Practice to return either true or false when there are only side effects happening inside a method.
    },
    hide: function(){
        this.toggle_week_and_month_controls();
        $(this.deadlineSectionSelectControls).each(function(){
            $(this).attr('disabled', 'disabled');
        });
        $(this.reminders_block_id).hide();
    },
    show: function(){
        this.toggle_week_and_month_controls();
        $(this.deadlineSectionSelectControls).each(function(){
            $(this).removeAttr('disabled');
        });
        $(this.reminders_block_id).show();
    },
    toggle_week_and_month_controls: function(){
        var is_week = ($(this.frequencyPeriodControl).val() === "week");
        if(is_week){
            this.toggle_when_week_is_selected();
        }else{
            this.toggle_when_month_is_selected();
        }
    },
    toggle_when_month_is_selected: function(){
        $(this.month_block_class).show();
        $(this.week_block_class).hide();
    },
    toggle_when_week_is_selected: function(){
        $(this.week_block_class).show();
        $(this.month_block_class).hide();
    }
};

DW.ReminderDetails = function(){
    this.number_of_days_before_deadline = 'input[name=number_of_days_before_deadline]';
    this.number_of_days_after_deadline = 'input[name=number_of_days_after_deadline]';
};

DW.ReminderDetails.prototype = {
    init: function(){
        $(this.number_of_days_before_deadline).attr('maxlength', '3')
        $(this.number_of_days_after_deadline).attr('maxlength', '3')
        return true;
    }
};

var deadlineDetails = new DW.DeadlineDetails;
var reminderDetails = new DW.ReminderDetails;
$(document).ready(function() {
    deadlineDetails.init();
    reminderDetails.init();
    /*
    $(deadlineDetails.deadlineEnabledControl).change(function(){
        deadlineDetails.init();
    });
    */
    $(deadlineDetails.frequencyPeriodControl).change(function(){
        deadlineDetails.show();
    });
});
