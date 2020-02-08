# email-anomaly-tool
PRCO304 Final-year Project: Using Anomaly Detection To Discover Malicious Internal Email Activity

## What is this project about?

One of the big challenges of insider threat is preventing data exfiltration. There are many forms that this type of activity can take, but the one that this project is focussing on is email. The key goal of this project is to be able to identify emails that might suggest that this sort of malicious activity is taking place. This could be based on unusually large attachments, emails sent out to unusual domains, or the activity taking place outside of normal working hours.

My experience of working within an insider threat team is that a lot of analysts are using SIEM tools to attempt to detect this type of behaviour. There are many issues with this approach. The two main ones are that using "traditional" SIEM tools such as ArcSight can be time consuming, and that specific rulesets to detect known types of activity are required for this to work. Essentially, this means that the only types of activity that are flagged are those that analysts have either encountered or have been able to think up. There is some good reason for this, namely that the context of a specific business might determine whether a particular environment is malicious or not.

What the project does attempt to address is the issue of finding events that might not have been considered when designing rulesets; those events that insider threat analysts have not considered as a possibility. The approach adopted is unsupervised multivariate anomaly detection. Instead of using training data, which by its nature doesn't solve the issue described, this approach will compare captured email events against each other. By applying statistical analysis such as the Isolated Forest algorithm, outlier events can be isolated and alerts generated on them. Insider threat analysts will then have a starting point to further investigate these events.
