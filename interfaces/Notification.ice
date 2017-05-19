module ModuleNotification{

	interface GmailI{
		void sendMail(string msg);
	};

	interface TelegramI{
		void sendMsg(string msg);
	};


};
