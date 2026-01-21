package com.javaProducer.dto;

public class Transaction {
    private String transactionId;
    private String userId;
    private double amount;
    private long transactionTime;
    private String merchantId;
    private String transactionType;
    private String location;
    private String paymentMethod;
    private boolean isInternational;
    private String currency;

    public Transaction() {}

    public Transaction(String transactionId, String userId, double amount, long transactionTime,
                      String merchantId, String transactionType, String location,
                      String paymentMethod, boolean isInternational, String currency) {
        this.transactionId = transactionId;
        this.userId = userId;
        this.amount = amount;
        this.transactionTime = transactionTime;
        this.merchantId = merchantId;
        this.transactionType = transactionType;
        this.location = location;
        this.paymentMethod = paymentMethod;
        this.isInternational = isInternational;
        this.currency = currency;
    }

    // Getters
    public String getTransactionId() { return transactionId; }
    public String getUserId() { return userId; }
    public double getAmount() { return amount; }
    public long getTransactionTime() { return transactionTime; }
    public String getMerchantId() { return merchantId; }
    public String getTransactionType() { return transactionType; }
    public String getLocation() { return location; }
    public String getPaymentMethod() { return paymentMethod; }
    public boolean isInternational() { return isInternational; }
    public String getCurrency() { return currency; }

    // Setters
    public void setTransactionId(String transactionId) { this.transactionId = transactionId; }
    public void setUserId(String userId) { this.userId = userId; }
    public void setAmount(double amount) { this.amount = amount; }
    public void setTransactionTime(long transactionTime) { this.transactionTime = transactionTime; }
    public void setMerchantId(String merchantId) { this.merchantId = merchantId; }
    public void setTransactionType(String transactionType) { this.transactionType = transactionType; }
    public void setLocation(String location) { this.location = location; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }
    public void setInternational(boolean international) { isInternational = international; }
    public void setCurrency(String currency) { this.currency = currency; }

    @Override
    public String toString() {
        return "Transaction{" +
                "transactionId='" + transactionId + '\'' +
                ", userId='" + userId + '\'' +
                ", amount=" + amount +
                ", transactionTime=" + transactionTime +
                ", merchantId='" + merchantId + '\'' +
                ", transactionType='" + transactionType + '\'' +
                ", location='" + location + '\'' +
                ", paymentMethod='" + paymentMethod + '\'' +
                ", isInternational=" + isInternational +
                ", currency='" + currency + '\'' +
                '}';
    }
}