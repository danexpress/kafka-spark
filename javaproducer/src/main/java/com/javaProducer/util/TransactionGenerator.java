package com.javaProducer.util;

import com.javaProducer.dto.Transaction;
import java.util.Random;
import java.util.UUID;

public class TransactionGenerator {

    private static final Random random = new Random();
    private static final String[] TRANSACTION_TYPES = {"purchase", "refund", "withdrawal", "deposit"};
    private static final String[] LOCATIONS = {"NY, USA", "LA, USA", "Chicago, USA", "Miami, USA"};
    private static final String[] PAYMENT_METHODS = {"credit_card", "debit_card", "paypal", "bank_transfer"};
    private static final String[] CURRENCIES = {"USD", "EUR", "GBP", "JPY"};

    public static Transaction randomTransaction() {
        Transaction transaction = new Transaction();
        transaction.setTransactionId(UUID.randomUUID().toString());
        transaction.setUserId("user-" + random.nextInt(1000));
        transaction.setAmount(Math.round((10 + (500 * random.nextDouble())) * 100.0) / 100.0);
        transaction.setTransactionTime(System.currentTimeMillis());
        transaction.setMerchantId("merchant-" + random.nextInt(100));
        transaction.setTransactionType(TRANSACTION_TYPES[random.nextInt(TRANSACTION_TYPES.length)]);
        transaction.setLocation(LOCATIONS[random.nextInt(LOCATIONS.length)]);
        transaction.setPaymentMethod(PAYMENT_METHODS[random.nextInt(PAYMENT_METHODS.length)]);
        transaction.setInternational(random.nextBoolean());
        transaction.setCurrency(CURRENCIES[random.nextInt(CURRENCIES.length)]);
        return transaction;
    }
}