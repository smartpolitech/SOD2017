module ModuleNotification{

	interface GmailI{
		bool sendMail(string date);
	};

	interface TelegramI{
		bool sendMsg(string date);
	};


};
