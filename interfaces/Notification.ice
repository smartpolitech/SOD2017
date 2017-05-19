module ModuleNotification{

	interface GmailI{
		void sendMail(string date);
	};

	interface TelegramI{
		void sendMsg(string date);
	};


};
