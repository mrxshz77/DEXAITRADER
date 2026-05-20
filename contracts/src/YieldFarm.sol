// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title YieldFarm
 * @author DEXAITRADER
 * @notice Yield farming and liquidity pool management contract
 * @dev Handles LP token staking, reward distribution, and yield optimization
 */

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

interface IUniswapV2Router {
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB, uint liquidity);
    
    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint liquidity,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB);
}

contract YieldFarm {
    
    // ================================
    // STRUCTS
    // ================================
    
    struct Pool {
        address lpToken;
        address rewardToken;
        uint256 totalStaked;
        uint256 rewardPerBlock;
        uint256 lastRewardBlock;
        uint256 accRewardPerShare;
        bool active;
    }
    
    struct UserInfo {
        uint256 amount;
        uint256 rewardDebt;
        uint256 stakedAt;
    }
    
    struct HarvestInfo {
        uint256 poolId;
        address user;
        uint256 amount;
        uint256 harvestedAt;
    }
    
    // ================================
    // STATE VARIABLES
    // ================================
    
    address public owner;
    
    uint256 public poolCounter;
    uint256 public constant BLOCKS_PER_YEAR = 2628000; // ~365 days * 24h * 3600s / 12s blocks
    
    mapping(uint256 => Pool) public pools;
    mapping(uint256 => mapping(address => UserInfo)) public userInfo;
    mapping(uint256 => mapping(address => HarvestInfo[])) public harvestHistory;
    
    uint256 public totalRewardsDistributed;
    uint256 public totalUsersParticipating;
    
    // ================================
    // EVENTS
    // ================================
    
    event PoolCreated(
        uint256 indexed poolId,
        address lpToken,
        address rewardToken,
        uint256 rewardPerBlock
    );
    
    event Staked(
        uint256 indexed poolId,
        address indexed user,
        uint256 amount
    );
    
    event Unstaked(
        uint256 indexed poolId,
        address indexed user,
        uint256 amount
    );
    
    event HarvestedRewards(
        uint256 indexed poolId,
        address indexed user,
        uint256 rewards
    );
    
    event PoolUpdated(
        uint256 indexed poolId,
        uint256 newRewardPerBlock
    );
    
    // ================================
    // MODIFIERS
    // ================================
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    modifier poolExists(uint256 poolId) {
        require(poolId < poolCounter, "Pool not found");
        require(pools[poolId].active, "Pool inactive");
        _;
    }
    
    // ================================
    // CONSTRUCTOR
    // ================================
    
    constructor() {
        owner = msg.sender;
    }
    
    // ================================
    // POOL MANAGEMENT
    // ================================
    
    /**
     * @notice Create a new yield farming pool
     * @param lpToken Address of LP token
     * @param rewardToken Address of reward token
     * @param rewardPerBlock Reward amount per block
     */
    function createPool(
        address lpToken,
        address rewardToken,
        uint256 rewardPerBlock
    ) external onlyOwner returns (uint256 poolId) {
        require(lpToken != address(0), "Invalid LP token");
        require(rewardToken != address(0), "Invalid reward token");
        
        poolId = poolCounter++;
        
        pools[poolId] = Pool({
            lpToken: lpToken,
            rewardToken: rewardToken,
            totalStaked: 0,
            rewardPerBlock: rewardPerBlock,
            lastRewardBlock: block.number,
            accRewardPerShare: 0,
            active: true
        });
        
        emit PoolCreated(poolId, lpToken, rewardToken, rewardPerBlock);
    }
    
    /**
     * @notice Update pool reward rate
     */
    function updatePoolRewardRate(uint256 poolId, uint256 newRewardPerBlock) external onlyOwner poolExists(poolId) {
        Pool storage pool = pools[poolId];
        _updatePool(poolId);
        pool.rewardPerBlock = newRewardPerBlock;
        emit PoolUpdated(poolId, newRewardPerBlock);
    }
    
    /**
     * @notice Deactivate a pool
     */
    function deactivatePool(uint256 poolId) external onlyOwner poolExists(poolId) {
        pools[poolId].active = false;
    }
    
    // ================================
    // STAKING FUNCTIONS
    // ================================
    
    /**
     * @notice Stake LP tokens to earn rewards
     * @param poolId ID of the pool
     * @param amount Amount of LP tokens to stake
     */
    function stake(uint256 poolId, uint256 amount) external poolExists(poolId) {
        require(amount > 0, "Cannot stake 0");
        
        Pool storage pool = pools[poolId];
        UserInfo storage user = userInfo[poolId][msg.sender];
        
        // Update pool rewards
        _updatePool(poolId);
        
        // Transfer LP tokens from user
        require(
            IERC20(pool.lpToken).transferFrom(msg.sender, address(this), amount),
            "Transfer failed"
        );
        
        // If user is new, increment counter
        if (user.amount == 0) {
            totalUsersParticipating++;
        }
        
        // Harvest pending rewards
        _harvestRewards(poolId, msg.sender);
        
        // Update user info
        user.amount += amount;
        user.rewardDebt = (user.amount * pool.accRewardPerShare) / 1e18;
        user.stakedAt = block.timestamp;
        
        pool.totalStaked += amount;
        
        emit Staked(poolId, msg.sender, amount);
    }
    
    /**
     * @notice Unstake LP tokens
     * @param poolId ID of the pool
     * @param amount Amount to unstake
     */
    function unstake(uint256 poolId, uint256 amount) external poolExists(poolId) {
        require(amount > 0, "Cannot unstake 0");
        
        Pool storage pool = pools[poolId];
        UserInfo storage user = userInfo[poolId][msg.sender];
        
        require(user.amount >= amount, "Insufficient staked amount");
        
        // Update pool rewards
        _updatePool(poolId);
        
        // Harvest pending rewards
        _harvestRewards(poolId, msg.sender);
        
        // Update user info
        user.amount -= amount;
        user.rewardDebt = (user.amount * pool.accRewardPerShare) / 1e18;
        
        pool.totalStaked -= amount;
        
        // Transfer LP tokens back to user
        require(
            IERC20(pool.lpToken).transfer(msg.sender, amount),
            "Transfer failed"
        );
        
        emit Unstaked(poolId, msg.sender, amount);
    }
    
    // ================================
    // REWARD HARVESTING
    // ================================
    
    /**
     * @notice Harvest accumulated rewards
     */
    function harvestRewards(uint256 poolId) external poolExists(poolId) {
        _harvestRewards(poolId, msg.sender);
    }
    
    function _harvestRewards(uint256 poolId, address user) internal {
        Pool storage pool = pools[poolId];
        UserInfo storage userData = userInfo[poolId][user];
        
        uint256 pending = (userData.amount * pool.accRewardPerShare) / 1e18 - userData.rewardDebt;
        
        if (pending > 0) {
            // Transfer reward tokens
            require(
                IERC20(pool.rewardToken).transfer(user, pending),
                "Reward transfer failed"
            );
            
            // Record harvest
            harvestHistory[poolId][user].push(HarvestInfo({
                poolId: poolId,
                user: user,
                amount: pending,
                harvestedAt: block.timestamp
            }));
            
            totalRewardsDistributed += pending;
            
            emit HarvestedRewards(poolId, user, pending);
        }
    }
    
    // ================================
    // INTERNAL FUNCTIONS
    // ================================
    
    /**
     * @notice Update pool's accumulated reward per share
     */
    function _updatePool(uint256 poolId) internal {
        Pool storage pool = pools[poolId];
        
        if (block.number <= pool.lastRewardBlock) return;
        
        uint256 blockCount = block.number - pool.lastRewardBlock;
        uint256 reward = blockCount * pool.rewardPerBlock;
        
        if (pool.totalStaked > 0) {
            pool.accRewardPerShare += (reward * 1e18) / pool.totalStaked;
        }
        
        pool.lastRewardBlock = block.number;
    }
    
    // ================================
    // GETTERS
    // ================================
    
    function getPool(uint256 poolId) external view returns (Pool memory) {
        return pools[poolId];
    }
    
    function getUserInfo(uint256 poolId, address user) external view returns (UserInfo memory) {
        return userInfo[poolId][user];
    }
    
    function getPendingRewards(uint256 poolId, address user) external view returns (uint256) {
        Pool storage pool = pools[poolId];
        UserInfo storage userdata = userInfo[poolId][user];
        
        uint256 accRewardPerShare = pool.accRewardPerShare;
        if (block.number > pool.lastRewardBlock && pool.totalStaked > 0) {
            uint256 blockCount = block.number - pool.lastRewardBlock;
            uint256 reward = blockCount * pool.rewardPerBlock;
            accRewardPerShare += (reward * 1e18) / pool.totalStaked;
        }
        
        return (userdata.amount * accRewardPerShare) / 1e18 - userdata.rewardDebt;
    }
    
    function getUserHarvestHistory(uint256 poolId, address user) external view returns (HarvestInfo[] memory) {
        return harvestHistory[poolId][user];
    }
    
    function getAPY(uint256 poolId) external view returns (uint256) {
        require(poolId < poolCounter, "Pool not found");
        Pool storage pool = pools[poolId];
        
        if (pool.totalStaked == 0) return 0;
        
        uint256 yearlyRewards = pool.rewardPerBlock * BLOCKS_PER_YEAR;
        return (yearlyRewards * 100) / pool.totalStaked;
    }
}
