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
    this.deadline_example = '#deadline_example'
};

DW.DeadlineDetails.prototype = {
    init: function() {
        this.show();
        this.update_example();
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
    },
    update_example: function(){
        var deadline_example = "";
        var frequency = $(this.frequencyPeriodControl).val();
        var deadline_type_value = $(this.deadlineTypeControl).val();
        if (frequency == 'week') {
            var selected_weekday_text = $(this.deadlineWeekControl+" :selected").text();
            if (deadline_type_value == 'Following') {
                deadline_example = interpolate(gettext("Example: %(day)s of the week following the reporting week"), { day : selected_weekday_text}, true);
            } else {
                deadline_example = interpolate(gettext("Example: %(day)s of the reporting week"), { day : selected_weekday_text }, true);
            }
        } else if (frequency == 'month') {
            var selected_month_day_text = $(this.deadlineMonthControl+" :selected").text();
            if (deadline_type_value == 'Following') {
                deadline_example = interpolate(gettext("Example: %(day)s of October for September report"), { day : selected_month_day_text }, true);
            } else {
                deadline_example = interpolate(gettext("Example: %(day)s of October for October report"), { day : selected_month_day_text }, true);
            }
        }
        $(this.deadline_example).html(deadline_example);

    }
};

DW.ReminderDetails = function(){
    this.number_of_days_before_deadline = 'input[name=number_of_days_before_deadline]';
    this.number_of_days_after_deadline = 'input[name=number_of_days_after_deadline]';
};

DW.ReminderDetails.prototype = {
    init: function(){
        $(this.number_of_days_before_deadline).attr('maxlength', '3');
        $(this.number_of_days_after_deadline).attr('maxlength', '3');
        return true;
    }
};

var deadlineDetails = new DW.DeadlineDetails;
var reminderDetails = new DW.ReminderDetails;
$(document).ready(function() {
    deadlineDetails.init();
    reminderDetails.init();
    $(deadlineDetails.frequencyPeriodControl).change(function(){
        deadlineDetails.show();
        deadlineDetails.update_example();
    });
    $(deadlineDetails.deadlineWeekControl).change(function(){
        deadlineDetails.update_example();
    });
    $(deadlineDetails.deadlineMonthControl).change(function(){
        deadlineDetails.update_example();
    });
    $(deadlineDetails.deadlineTypeControl).change(function(){
        deadlineDetails.update_example();
    });
});
