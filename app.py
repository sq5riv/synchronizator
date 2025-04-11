from time import sleep
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from src.synchronizator import Synchronizator
from src.utils import Utils, logger


def main() -> None:
    args = Utils.argument_parser().parse_args()
    Utils.set_logger(args.log_file)
    synchronizator = Synchronizator(args.source_folder, args.replica_folder)
    scheduler = BackgroundScheduler()
    scheduler.add_job(synchronizator,
                      'interval',
                      seconds=Utils.time_parser(args.synchronization_interval),
                      next_run_time=datetime.now())

    scheduler.start()

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info('Synchronization stopped. Thank you for using our software. Good Bye!')


if __name__ == '__main__':
    main()
